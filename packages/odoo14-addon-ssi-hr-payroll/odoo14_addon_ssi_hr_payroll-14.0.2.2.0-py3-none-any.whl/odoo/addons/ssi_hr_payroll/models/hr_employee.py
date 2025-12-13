# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee Input"

    salary_structure_id = fields.Many2one(
        string="Salary Structure",
        comodel_name="hr.salary_structure",
    )
    input_line_ids = fields.One2many(
        string="Input Types",
        comodel_name="hr.employee_input",
        inverse_name="employee_id",
    )
