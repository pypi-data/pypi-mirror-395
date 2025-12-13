# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from pytz import timezone

import odoo
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

from odoo.addons.ssi_decorator import ssi_decorator


class BrowsableObject(object):
    def __init__(self, employee_id, vals_dict, env):
        self.employee_id = employee_id
        self.dict = vals_dict
        self.env = env

    def __getattr__(self, attr):
        return attr in self.dict and self.dict.__getitem__(attr) or 0.0


class Payslips(BrowsableObject):
    """a class that will be used into the python code, mainly for
    usability purposes"""

    def sum(self, code, from_date, to_date=None):
        if to_date is None:
            to_date = fields.Date.today()
        self.env.cr.execute(
            """SELECT sum(case when hp.credit_note = False then
            (pl.total) else (-pl.total) end)
                    FROM hr_payslip as hp, hr_payslip_line as pl
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND
                     hp.id = pl.slip_id AND pl.code = %s""",
            (self.employee_id, from_date, to_date, code),
        )
        res = self.env.cr.fetchone()
        return res and res[0] or 0.0


class InputLine(BrowsableObject):
    """a class that will be used into the python code, mainly for
    usability purposes"""

    def sum(self, code, from_date, to_date=None):
        if to_date is None:
            to_date = fields.Date.today()
        self.env.cr.execute(
            """
            SELECT sum(amount) as sum
            FROM hr_payslip as hp, hr_payslip_input as pi
            WHERE hp.employee_id = %s AND hp.state = 'done'
            AND hp.date_from >= %s AND hp.date_to <= %s
            AND hp.id = pi.payslip_id AND pi.code = %s""",
            (self.employee_id, from_date, to_date, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class EmployeeInputLine(BrowsableObject):
    def sum(self, code):
        self.env.cr.execute(
            """
            SELECT sum(b.amount) as sum
            FROM hr_employee as a
            JOIN hr_employee_input as b ON a.id=b.employee_id
            JOIN hr_employee_input_type as c ON b.input_type_id=c.id
            WHERE a.id = %s AND c.code = %s""",
            (self.employee_id, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class HrPayslip(models.Model):
    _name = "hr.payslip"
    _description = "Employee Payslip"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.employee_document",
        "mixin.date_duration",
    ]
    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Sequence attribute
    _create_sequence_state = "done"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.payslip_type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    structure_id = fields.Many2one(
        string="Salary Structure",
        comodel_name="hr.salary_structure",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    rule_ids = fields.Many2many(
        string="All Salary Rules",
        comodel_name="hr.salary_rule",
        compute="_compute_rule_ids",
        store=False,
    )
    line_ids = fields.One2many(
        string="Payslip Lines",
        comodel_name="hr.payslip_line",
        inverse_name="payslip_id",
        readonly=True,
        copy=False,
    )
    input_line_ids = fields.One2many(
        string="Input Types",
        comodel_name="hr.payslip_input",
        inverse_name="payslip_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=True,
    )
    allowed_allowance_move_line_ids = fields.Many2many(
        string="Allowed Allowance Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_allowance_move_line_ids",
        store=False,
    )

    allowance_ref_move_line_ids = fields.Many2many(
        string="Allowance Ref Move Lines",
        comodel_name="account.move.line",
        relation="rel_payslip_2_allowance_ml",
        column1="payslip_id",
        column2="move_line_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_deduction_move_line_ids = fields.Many2many(
        string="Allowed Deduction Ref Move Lines",
        comodel_name="account.move.line",
        compute="_compute_allowed_deduction_move_line_ids",
        store=False,
    )
    deduction_ref_move_line_ids = fields.Many2many(
        string="Deduction Ref Move Lines",
        comodel_name="account.move.line",
        relation="rel_payslip_2_deduction_ml",
        column1="payslip_id",
        column2="move_line_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    debit_account_2b_reconciled_ids = fields.Many2many(
        string="Debit Accounts To Be Reconciled",
        comodel_name="account.account",
        compute="_compute_debit_account_2b_reconciled_ids",
        store=False,
    )
    credit_account_2b_reconciled_ids = fields.Many2many(
        string="Credit Accounts To Be Reconciled",
        comodel_name="account.account",
        compute="_compute_credit_account_2b_reconciled_ids",
        store=False,
    )
    move_id = fields.Many2one(
        string="# Accounting Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    move_line_debit_id = fields.Many2one(
        string="Move Line Debit",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    move_line_credit_id = fields.Many2one(
        string="Move Line Credit",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.depends(
        "structure_id",
    )
    def _compute_rule_ids(self):
        for record in self:
            result = []
            if record.structure_id:
                structures = record.structure_id._get_parent_structure()
                rule_list = structures.get_all_rules()
                result = [id for id, sequence in sorted(rule_list, key=lambda x: x[1])]
            record.rule_ids = result

    @api.depends(
        "rule_ids",
    )
    def _compute_debit_account_2b_reconciled_ids(self):
        SalaryRule = self.env["hr.salary_rule"]
        for record in self:
            result = []
            criteria = [
                ("id", "in", record.rule_ids.ids),
                ("reconcile_debit_account_id", "!=", False),
                ("reconcile_debit", "=", True),
            ]
            for rule in SalaryRule.search(criteria):
                result.append(rule.reconcile_debit_account_id.id)
            record.debit_account_2b_reconciled_ids = result

    @api.depends(
        "rule_ids",
    )
    def _compute_credit_account_2b_reconciled_ids(self):
        SalaryRule = self.env["hr.salary_rule"]
        for record in self:
            result = []
            criteria = [
                ("id", "in", record.rule_ids.ids),
                ("reconcile_credit_account_id", "!=", False),
                ("reconcile_credit", "=", True),
            ]
            for rule in SalaryRule.search(criteria):
                result.append(rule.reconcile_credit_account_id.id)
            record.credit_account_2b_reconciled_ids = result

    @api.depends(
        "employee_id",
        "structure_id",
    )
    def _compute_allowed_deduction_move_line_ids(self):
        ML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.employee_id and record.structure_id:
                criteria = [
                    ("partner_id", "=", record.employee_id.address_home_id.id),
                    ("account_id", "in", record.credit_account_2b_reconciled_ids.ids),
                    ("debit", ">", 0.0),
                    ("reconciled", "=", False),
                ]
                result = ML.search(criteria).ids
            record.allowed_deduction_move_line_ids = result

    @api.depends(
        "employee_id",
        "structure_id",
    )
    def _compute_allowed_allowance_move_line_ids(self):
        ML = self.env["account.move.line"]
        for record in self:
            result = []
            if record.employee_id and record.structure_id:
                criteria = [
                    ("partner_id", "=", record.employee_id.address_home_id.id),
                    ("account_id", "in", record.debit_account_2b_reconciled_ids.ids),
                    ("credit", ">", 0.0),
                    ("reconciled", "=", False),
                ]
                result = ML.search(criteria).ids
            record.allowed_allowance_move_line_ids = result

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "structure_id",
    )
    def onchange_input_line_ids(self):
        res = []
        self.input_line_ids = False
        if self.structure_id:
            input_line_ids = self._get_input_line_ids()
            if input_line_ids:
                for input_line in input_line_ids:
                    res.append((0, 0, input_line))
        self.input_line_ids = res

    @api.onchange(
        "employee_id",
    )
    def onchange_structure_id(self):
        self.structure_id = False
        if self.employee_id:
            self.structure_id = self.employee_id.salary_structure_id

    def action_recompute_allowance_ref(self):
        for record in self.sudo():
            record._recompute_allowance_ref()

    def action_recompute_deduction_ref(self):
        for record in self.sudo():
            record._recompute_deduction_ref()

    def action_reload_input_lines(self):
        for record in self.sudo():
            record._reload_input_lines()

    def action_compute_payslip(self):
        for document in self.sudo():
            document._recompute_allowance_ref()
            document._recompute_deduction_ref()
            document._compute_payslip()

    @ssi_decorator.post_cancel_action()
    def _10_cancel_accounting_entry(self):
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]

        if not self.move_id:
            return True

        move = self.move_id

        if self.move_id.state == "posted":
            self.move_id.button_cancel()

        self.write(
            {
                "move_line_debit_id": False,
                "move_line_credit_id": False,
                "move_id": False,
            }
        )

        debit_criteria = [
            ("payslip_id", "=", self.id),
            ("move_line_debit_id", "!=", False),
            ("rule_id.reconcile_debit", "=", True),
        ]
        for line in PayslipLine.search(debit_criteria):
            line._unreconcile_debit()

        credit_criteria = [
            ("payslip_id", "=", self.id),
            ("move_line_credit_id", "!=", False),
            ("rule_id.reconcile_credit", "=", True),
        ]
        for line in PayslipLine.search(credit_criteria):
            line._unreconcile_credit()

        for line in self.line_ids:
            line.write(
                {
                    "move_line_debit_id": False,
                    "move_line_credit_id": False,
                }
            )
        move.with_context(force_delete=True).unlink()

    @ssi_decorator.post_done_action()
    def _10_create_accounting_entry(self):
        Move = self.env["account.move"]
        ML = self.env["account.move.line"]

        currency = self.company_id.currency_id or self.journal_id.company_id.currency_id
        move = Move.create(self._prepare_account_move_data())
        self.move_id = move.id
        debit_sum, credit_sum = self.line_ids.create_move_line(move)

        if currency.compare_amounts(credit_sum, debit_sum) == -1:
            move_line = ML.create(
                self._prepare_adjustment_aml_data(
                    currency, credit_sum, debit_sum, move, "credit"
                )
            )
            self.move_line_credit_id = move_line.id
        elif currency.compare_amounts(debit_sum, credit_sum) == -1:
            move_line = ML.create(
                self._prepare_adjustment_aml_data(
                    currency, credit_sum, debit_sum, move, "debit"
                )
            )
            self.move_line_debit_id = move_line.id

        move.action_post()
        self._reconcile_debit_payslip_line()
        self._reconcile_credit_payslip_line()

    def _compute_payslip(self):
        self.ensure_one()
        self.line_ids.unlink()
        self.write(self._prepare_payslip_line_data())

    def _recompute_allowance_ref(self):
        self.ensure_one()
        ML = self.env["account.move.line"]
        criteria = [
            "&",
            "|",
            "&",
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            "&",
            ("date_maturity", ">=", self.date_start),
            ("date_maturity", "<=", self.date_end),
            ("id", "in", self.allowed_allowance_move_line_ids.ids),
        ]
        move_lines = ML.search(criteria)
        self.write({"allowance_ref_move_line_ids": [(6, 0, move_lines.ids)]})

    def _recompute_deduction_ref(self):
        self.ensure_one()
        ML = self.env["account.move.line"]
        criteria = [
            "&",
            "|",
            "&",
            "&",
            ("date_maturity", "=", False),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            "&",
            ("date_maturity", ">=", self.date_start),
            ("date_maturity", "<=", self.date_end),
            ("id", "in", self.allowed_deduction_move_line_ids.ids),
        ]
        move_lines = ML.search(criteria)
        self.write({"deduction_ref_move_line_ids": [(6, 0, move_lines.ids)]})

    @api.model
    def _get_policy_field(self):
        res = super(HrPayslip, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _prepare_payslip_line_data(self):
        self.ensure_one()
        lines = [(0, 0, line) for line in self._get_payslip_lines(self.id)]
        return {"line_ids": lines}

    def _prepare_account_move_data(self):
        self.ensure_one()
        name = _("Payslip of %s") % (self.employee_id.name)
        data = {
            "narration": name,
            "ref": self.name,
            "name": self.name,
            "journal_id": self.journal_id.id,
            "date": self.date or self.date_to,
        }
        return data

    def _prepare_adjustment_aml_data(
        self, currency, credit_sum, debit_sum, move_id, type_data
    ):
        self.ensure_one()
        journal_acc_id = self.journal_id.default_account_id.id
        if not journal_acc_id:
            msgError = _(
                "The Expense Journal %s has not properly "
                "configured the Credit or Debit Account!"
            )
            raise UserError(msgError % (self.journal_id.name))

        data = {
            "move_id": move_id.id,
            "name": _("Adjustment Entry"),
            "partner_id": False,
            "account_id": journal_acc_id,
            "journal_id": self.journal_id.id,
            "date": self.date,
        }
        if type_data == "debit":
            data["debit"] = currency.round(credit_sum - debit_sum)
            data["credit"] = 0.0
        else:
            data["credit"] = currency.round(debit_sum - credit_sum)
            data["debit"] = 0.0
        return data

    def _sum_salary_rule_category(self, localdict, category, amount):
        self.ensure_one()
        if category.parent_id:
            localdict = self._sum_salary_rule_category(
                localdict, category.parent_id, amount
            )

        if category.code in localdict["categories"].dict:
            localdict["categories"].dict[category.code] += amount
        else:
            localdict["categories"].dict[category.code] = amount

        return localdict

    def _get_salary_rules(self):
        self.ensure_one()
        obj_hr_salary_rule = self.env["hr.salary_rule"]
        obj_hr_salary_struc = self.env["hr.salary_structure"]
        rule_ids = []
        if self.structure_id.id:
            structure_ids = obj_hr_salary_struc.browse(
                self.structure_id.id
            )._get_parent_structure()
            rule_ids = structure_ids.get_all_rules()
            sorted_rule_ids = [
                id for id, sequence in sorted(rule_ids, key=lambda x: x[1])
            ]
            rule_ids = obj_hr_salary_rule.browse(sorted_rule_ids)
        return rule_ids

    def _get_base_localdict(self, payslip):
        self.ensure_one()
        inputs_dict = {}
        emp_inputs_dict = {}
        baselocaldict = {
            "env": self.env,
            "time": tools.safe_eval.time,
            "datetime": tools.safe_eval.datetime,
            "dateutil": tools.safe_eval.dateutil,
            "timezone": timezone,
            "float_compare": float_compare,
            "UserError": odoo.exceptions.UserError,
        }

        categories = BrowsableObject(payslip.employee_id.id, {}, self.env)
        if categories:
            baselocaldict["categories"] = categories

        for input_line in self.input_line_ids:
            inputs_dict[input_line.input_type_id.code] = input_line
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        if inputs:
            baselocaldict["inputs"] = inputs

        for emp_input_line in self.employee_id.input_line_ids:
            emp_inputs_dict[emp_input_line.input_type_id.code] = emp_input_line
        emp_inputs = EmployeeInputLine(
            payslip.employee_id.id, emp_inputs_dict, self.env
        )
        if emp_inputs:
            baselocaldict["emp_inputs"] = emp_inputs

        payslips = Payslips(payslip.employee_id.id, self, self.env)
        if payslips:
            baselocaldict["payslip"] = payslips

        rules = BrowsableObject(payslip.employee_id.id, {}, self.env)
        if rules:
            baselocaldict["rules"] = rules

        return baselocaldict

    @api.model
    def _get_payslip_lines(self, payslip_id):
        self.ensure_one()
        result_dict = {}
        rules_dict = {}
        blacklist = []

        obj_hr_payslip = self.env["hr.payslip"]

        employee = self.employee_id

        payslip = obj_hr_payslip.browse(payslip_id)

        baselocaldict = self._get_base_localdict(payslip)

        sorted_rules = self._get_salary_rules()

        localdict = dict(baselocaldict, employee=employee)
        for rule in sorted_rules:
            key = rule.code
            localdict["result"] = None
            localdict["result_qty"] = 1.0
            localdict["result_rate"] = 100
            if rule._evaluate_rule("condition", localdict) and rule.id not in blacklist:
                amount, qty, rate = rule._evaluate_rule("amount", localdict)
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                tot_rule = amount * qty * rate / 100.0
                localdict[rule.code] = tot_rule
                rules_dict[rule.code] = rule
                localdict = self._sum_salary_rule_category(
                    localdict, rule.category_id, tot_rule - previous_amount
                )
                result_dict[key] = {
                    "payslip_id": payslip_id,
                    "rule_id": rule.id,
                    "amount": amount,
                    "quantity": qty,
                    "rate": rate,
                }
            else:
                blacklist += [id for id, seq in rule._recursive_search_of_rules()]

        return list(result_dict.values())

    def _get_input_line_ids(self):
        self.ensure_one()
        res = []
        obj_hr_salary_struc = self.env["hr.salary_structure"]
        obj_hr_salary_rule = self.env["hr.salary_rule"]

        structure_id = self.structure_id.id

        structure_ids = obj_hr_salary_struc.browse(structure_id)._get_parent_structure()
        rule_ids = structure_ids.get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        input_type_ids = obj_hr_salary_rule.browse(sorted_rule_ids).mapped(
            "input_type_ids"
        )
        for input_type in input_type_ids:
            res.append(
                {
                    "input_type_id": input_type.id,
                }
            )
        return res

    def _reload_input_lines(self):
        self.ensure_one()
        self.onchange_input_line_ids()

    def _reconcile_debit_payslip_line(self):
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]
        criteria = [
            ("payslip_id", "=", self.id),
            ("rule_id.reconcile_debit", "=", True),
        ]
        for detail in PayslipLine.search(criteria):
            detail._reconcile_debit()

    def _reconcile_credit_payslip_line(self):
        self.ensure_one()
        PayslipLine = self.env["hr.payslip_line"]
        criteria = [
            ("payslip_id", "=", self.id),
            ("rule_id.reconcile_credit", "=", True),
        ]
        for detail in PayslipLine.search(criteria):
            detail._reconcile_credit()
