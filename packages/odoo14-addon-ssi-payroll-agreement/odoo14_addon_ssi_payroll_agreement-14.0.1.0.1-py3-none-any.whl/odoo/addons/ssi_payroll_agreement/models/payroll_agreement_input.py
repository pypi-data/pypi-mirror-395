# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class PayrollAgreementInput(models.Model):
    _name = "payroll_agreement_input"

    _description = "Payroll Agreement Input"

    payroll_agreement_id = fields.Many2one(
        string="Payroll Agreement",
        comodel_name="payroll_agreement",
        required=True,
        ondelete="cascade",
    )
    input_type_id = fields.Many2one(
        string="Input Type",
        comodel_name="payroll_agreement_input_type",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
        required=True,
        default=0.0,
    )
