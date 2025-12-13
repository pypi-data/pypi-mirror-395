# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrPayslipType(models.Model):
    _name = "hr.payslip_type"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Payslip Type"

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        ondelete="restrict",
    )
