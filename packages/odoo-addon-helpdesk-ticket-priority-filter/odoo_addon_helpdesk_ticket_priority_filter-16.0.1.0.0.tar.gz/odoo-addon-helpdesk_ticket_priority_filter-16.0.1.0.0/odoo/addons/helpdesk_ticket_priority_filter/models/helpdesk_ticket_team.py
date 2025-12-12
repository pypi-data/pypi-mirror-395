from odoo import api, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    @api.depends("ticket_ids", "ticket_ids.stage_id")
    def _compute_todo_tickets(self):
        result = super()._compute_todo_tickets()
        ticket_model = self.env["helpdesk.ticket"]
        fetch_data = ticket_model.read_group(
            [("team_id", "in", self.ids), ("closed", "=", False)],
            ["team_id", "priority"],
            ["team_id", "priority"],
            lazy=False,
        )
        result = [
            [
                data["team_id"][0],
                data["priority"],
                data["__count"],
            ]
            for data in fetch_data
        ]
        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()
        for team in self:
            team.todo_ticket_count_high_priority = sum(
                r[2] for r in result if r[0] == team.id and r[1] in high_priority_levels
            )
