from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    is_high_priority = fields.Boolean(
        string="Is High Priority",
        compute="_compute_is_high_priority",
        search="_search_is_high_priority",
        default=False,
    )

    def _search_is_high_priority(self, operator, value):
        high_priority_levels = self._get_high_priority_levels()

        if (operator == "=" and value) or (operator == "!=" and not value):
            return [("priority", "in", high_priority_levels)]
        else:
            return [("priority", "not in", high_priority_levels)]

    @api.depends("priority")
    def _compute_is_high_priority(self):
        high_priority_levels = self._get_high_priority_levels()
        for ticket in self:
            ticket.is_high_priority = ticket.priority in high_priority_levels

    def _get_high_priority_levels(self):
        """Get levels configured as high priority from system parameters.
        Only return those configured levels that are valid priorities.
        """
        params = self.env["ir.config_parameter"].sudo()
        levels_str = params.get_param(
            "helpdesk_ticket_priority_filter.high_priority_levels", "2,3"
        )
        configured_levels = [
            level.strip() for level in levels_str.split(",") if level.strip()
        ]
        valid_priorities = dict(self._fields["priority"].selection).keys()
        return [level for level in configured_levels if level in valid_priorities]
