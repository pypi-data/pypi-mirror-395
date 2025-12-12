# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHelpdeskTicketTeam(TransactionCase):
    def setUp(self):
        super().setUp()
        self.team = self.env.ref("helpdesk_mgmt.helpdesk_team_1")
        self.ticket = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "description": "This is a test ticket.",
                "priority": "1",
                "team_id": self.team.id,
            }
        )

    def test_team_todo_ticket_count_high_priority(self):
        """Test that the todo_ticket_count_high_priority field is computed correctly."""
        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()

        self.assertEqual(
            high_priority_levels,
            ["2", "3"],
            "High priority levels are ['2','3'] by default.",
        )
        self.assertFalse(self.ticket.priority in high_priority_levels)
        self.team._compute_todo_tickets()
        self.assertEqual(self.team.todo_ticket_count_high_priority, 0)

        # Change the ticket priority to a high priority level
        self.ticket.priority = "3"
        self.assertTrue(self.ticket.priority in high_priority_levels)
        self.team._compute_todo_tickets()
        self.assertEqual(self.team.todo_ticket_count_high_priority, 1)

        # Add another high priority ticket
        self.env["helpdesk.ticket"].create(
            {
                "name": "Another Test Ticket",
                "description": "This is another test ticket.",
                "priority": "3",
                "team_id": self.team.id,
            }
        )
        self.team._compute_todo_tickets()
        self.assertEqual(self.team.todo_ticket_count_high_priority, 2)
