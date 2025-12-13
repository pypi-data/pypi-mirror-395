# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    payroll_agreement_ids = fields.One2many(
        comodel_name="payroll_agreement",
        inverse_name="employee_id",
        string="Agreements",
    )

    @api.depends(
        "payroll_agreement_ids",
        "payroll_agreement_ids.state",
    )
    def _compute_payroll_agreement_id(self):
        for record in self:
            record.payroll_agreement_id = False
            active_agreement_id = record.payroll_agreement_ids.filtered(
                lambda x: x.state == "open"
            )
            if len(active_agreement_id) > 0:
                record.payroll_agreement_id = active_agreement_id[0]

    payroll_agreement_id = fields.Many2one(
        comodel_name="payroll_agreement",
        compute="_compute_payroll_agreement_id",
        string="Active Agreement",
        store=True,
        readonly=True,
        compute_sudo=True,
    )

    method = fields.Selection(
        string="Payroll Method",
        selection=[
            ("manual", "Manual"),
            ("agreement", "From Payroll Agreement"),
        ],
        default="manual",
    )
    manual_salary_structure_id = fields.Many2one(
        string="Manual Salary Structure",
        comodel_name="hr.salary_structure",
    )

    @api.depends(
        "method",
        "payroll_agreement_id",
        "manual_salary_structure_id",
    )
    def _compute_salary_structure_id(self):
        for record in self:
            record.salary_structure_id = record.manual_salary_structure_id
            if record.method == "agreement":
                record.salary_structure_id = (
                    record.payroll_agreement_id.salary_structure_id
                )

    salary_structure_id = fields.Many2one(
        comodel_name="hr.salary_structure",
        compute="_compute_salary_structure_id",
        store=True,
        compute_sudo=True,
    )
