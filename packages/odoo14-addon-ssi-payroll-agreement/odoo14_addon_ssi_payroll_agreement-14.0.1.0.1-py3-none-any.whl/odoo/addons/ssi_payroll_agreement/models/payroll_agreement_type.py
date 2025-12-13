# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PayrollAgreementType(models.Model):
    _name = "payroll_agreement_type"
    _description = "Payroll Agreement Type"
    _inherit = ["mixin.master_data"]

    name = fields.Char(
        string="Payroll Agreement Type",
    )
