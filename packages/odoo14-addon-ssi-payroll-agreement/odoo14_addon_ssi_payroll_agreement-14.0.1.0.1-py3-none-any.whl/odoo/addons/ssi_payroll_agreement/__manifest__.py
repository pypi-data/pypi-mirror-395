# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=C8101
{
    "name": "Payroll Agreement",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_hr_payroll",
        "ssi_transaction_ready_mixin",
        "ssi_transaction_open_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "menu.xml",
        "views/payroll_agreement_views.xml",
        "views/payroll_agreement_input_type_views.xml",
        "views/payroll_agreement_input_views.xml",
        "views/payroll_agreement_type_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_payslip_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
