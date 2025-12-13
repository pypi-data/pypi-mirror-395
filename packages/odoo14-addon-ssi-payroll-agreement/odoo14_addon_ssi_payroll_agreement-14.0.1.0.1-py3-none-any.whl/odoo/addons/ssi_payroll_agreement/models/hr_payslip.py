# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_hr_payroll.models.hr_payslip import BrowsableObject


class AgreementInputLine(BrowsableObject):
    def sum(self, code):
        self.env.cr.execute(
            """
            SELECT sum(b.amount) as sum
            FROM payroll_agreement as a
            JOIN payroll_agreement_input as b ON a.id=b.employee_id
            JOIN payroll_agreement_input_type as c ON b.input_type_id=c.id
            WHERE a.id = %s AND c.code = %s""",
            (self.employee_id, code),
        )
        return self.env.cr.fetchone()[0] or 0.0


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    payroll_agreement_id = fields.Many2one(
        string="Payroll Agreement",
        comodel_name="payroll_agreement",
        required=False,
    )
    method = fields.Selection(
        related="employee_id.method",
    )

    def _get_salary_rules(self):
        _super = super(HrPayslip, self)
        res = _super._get_salary_rules()
        if self.payroll_agreement_id:
            rule_ids = self.payroll_agreement_id.salary_rule_ids
            sorted_rule_ids = rule_ids.sorted(lambda x: x.sequence)
            res = sorted_rule_ids
        return res

    def _get_base_localdict(self, payslip):
        _super = super(HrPayslip, self)
        res = _super._get_base_localdict(payslip)
        aggr_inputs_dict = {}

        for aggr_input_line in self.payroll_agreement_id.input_line_ids:
            aggr_inputs_dict[aggr_input_line.input_type_id.code] = aggr_input_line

        aggr_inputs = AgreementInputLine(
            payslip.employee_id.id, aggr_inputs_dict, self.env
        )
        if aggr_inputs:
            res["aggr_inputs"] = aggr_inputs
        return res

    def _get_payroll_agreement(self):
        self.ensure_one()
        result = False

        if not self.employee_id.payroll_agreement_id:
            error_message = """
            Context: Payslip
            Problem: No active payroll agreement was found for employee %s.
            Solution: Please create and start a payroll agreement for this employee.
            """ % (
                self.employee_id.name
            )
            raise ValidationError(_(error_message))

        aggrements = self.employee_id.payroll_agreement_ids.filtered(
            lambda x: x.date <= self.date_start and x.state in ["open", "done"]
        )
        if aggrements:
            result = aggrements[0]
        else:
            error_message = """
            Context: Payslip
            Problem: No payroll agreement was found for %s on %s.
            Solution: Please create and start a payroll agreement for this employee.
            """ % (
                self.employee_id.name,
                self.date_start,
            )
            raise ValidationError(_(error_message))

        return result

    @api.onchange(
        "method",
        "date_start",
    )
    def onchange_payroll_agreement_id(self):
        self.payroll_agreement_id = False
        if self.method == "agreement" and self.date_start:
            self.payroll_agreement_id = self._get_payroll_agreement()

    @api.onchange(
        "payroll_agreement_id",
    )
    def onchange_aggrement_structure_id(self):
        if self.payroll_agreement_id:
            self.structure_id = self.payroll_agreement_id.salary_structure_id
        else:
            self.onchange_structure_id()

    @api.onchange(
        "employee_id",
    )
    def onchange_structure_id(self):
        self.structure_id = False
        if self.employee_id and self.method == "manual":
            self.structure_id = self.employee_id.salary_structure_id
