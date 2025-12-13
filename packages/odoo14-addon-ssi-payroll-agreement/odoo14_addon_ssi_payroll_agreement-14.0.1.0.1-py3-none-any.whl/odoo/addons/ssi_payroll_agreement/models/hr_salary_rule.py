# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class HrSalaryRule(models.Model):
    _inherit = "hr.salary_rule"

    @api.model
    def _default_condition_python(self):
        default = """# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories
#    (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days
# inputs: object containing the computed inputs
# emp_inputs: object containing the employee computed inputs.
# aggr_inputs: object containing the employee payroll agreement inputs.

# Note: returned value have to be set in the variable 'result'

result = True"""
        return default

    @api.model
    def _default_amount_python(self):
        default = """# Available variables:
#----------------------
# payslip: object containing the payslips
# employee: hr.employee object
# contract: hr.contract object
# rules: object containing the rules code (previously computed)
# categories: object containing the computed salary rule categories
#    (sum of amount of all rules belonging to that category).
# worked_days: object containing the computed worked days.
# inputs: object containing the computed inputs.
# emp_inputs: object containing the employee computed inputs.
# aggr_inputs: object containing the employee payroll agreement inputs.

# Note: returned value have to be set in the variable 'result'

result = True"""
        return default
