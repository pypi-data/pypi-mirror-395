# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class PayrollAgreement(models.Model):
    _name = "payroll_agreement"
    _inherit = [
        "mixin.employee_document",
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _description = "Payroll Agreement"
    _order = "employee_id, date desc"
    _approval_from_state = "draft"
    _approval_to_state = "ready"
    _approval_state = "confirm"
    _after_approved_method = "action_ready"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_ready_policy_fields = False
    _automatically_insert_ready_button = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,confirm,ready,open,done"

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "open_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_ready",
        "dom_open",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    _create_sequence_state = "ready"

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        comodel_name="payroll_agreement_type",
        string="Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    salary_structure_id = fields.Many2one(
        string="Salary Structure",
        comodel_name="hr.salary_structure",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    salary_rule_ids = fields.Many2many(
        string="Salary Rules",
        comodel_name="hr.salary_rule",
        relation="rel_payroll_agreement_2_salary_rule",
        column1="payroll_agreement_id",
        column2="salary_rule_id",
    )
    input_line_ids = fields.One2many(
        string="Input Types",
        comodel_name="payroll_agreement_input",
        inverse_name="payroll_agreement_id",
    )
    reference = fields.Char(
        string="Reference",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.model
    def _get_policy_field(self):
        res = super(PayrollAgreement, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    def action_populate_salary_rule_ids(self):
        for record in self:
            record._populate_salary_rule_ids()

    def _populate_salary_rule_ids(self):
        self.ensure_one()
        if self.salary_structure_id:
            rule_list = self.salary_structure_id.get_all_rules()
            rule_ids = [id for id, sequence in sorted(rule_list, key=lambda x: x[1])]
            if rule_ids:
                self.write({"salary_rule_ids": [(6, 0, rule_ids)]})

    @api.constrains(
        "state",
    )
    def _constrains_open(self):
        for record in self.sudo():
            if record.state != "open":
                break

            criteria = [
                ("id", "<>", record.id),
                ("employee_id", "=", record.employee_id.id),
                ("state", "=", "open"),
            ]
            check_open = self.search_count(criteria)
            if check_open > 0:
                error_message = """
                    Context: Check status in progress
                    Database ID: %s
                    Problem: There can only be one data with status In Progress for employee %s.
                    """ % (
                    record.id,
                    record.employee_id.name,
                )
                raise ValidationError(_(error_message))
