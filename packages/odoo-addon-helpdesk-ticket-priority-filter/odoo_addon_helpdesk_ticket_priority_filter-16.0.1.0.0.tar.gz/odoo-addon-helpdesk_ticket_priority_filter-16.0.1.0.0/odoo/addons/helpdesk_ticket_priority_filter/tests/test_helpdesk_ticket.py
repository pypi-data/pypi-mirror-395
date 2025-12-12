# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ticket = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "description": "This is a test ticket.",
                "priority": "1",
            }
        )

    def test_is_high_priority_field(self):
        """Test that the is_high_priority field is computed correctly."""
        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()

        self.assertFalse(self.ticket.priority in high_priority_levels)
        self.ticket._compute_is_high_priority()
        self.assertFalse(self.ticket.is_high_priority)

        # Change the ticket priority to a high priority level
        self.ticket.priority = high_priority_levels[0]
        self.ticket._compute_is_high_priority()
        self.assertTrue(self.ticket.is_high_priority)

    def test_search_is_high_priority(self):
        """Test the search method for is_high_priority field."""
        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()

        high_priority_tickets = self.env["helpdesk.ticket"].search(
            [("is_high_priority", "=", True)]
        )
        self.assertNotIn(self.ticket, high_priority_tickets)

        self.ticket.priority = high_priority_levels[0]
        self.ticket._compute_is_high_priority()

        high_priority_tickets = self.env["helpdesk.ticket"].search(
            [("is_high_priority", "=", True)]
        )
        self.assertIn(self.ticket, high_priority_tickets)

    def test_get_high_priority_levels(self):
        """Test that the _get_high_priority_levels method returns valid priorities."""
        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()
        valid_priorities = dict(
            self.env["helpdesk.ticket"]._fields["priority"].selection
        ).keys()

        for level in high_priority_levels:
            self.assertIn(level, valid_priorities)

    def test_get_high_priority_levels_with_invalid_values(self):
        """Test that invalid values are filtered out from configuration."""
        self.env["ir.config_parameter"].sudo().set_param(
            "helpdesk_ticket_priority_filter.high_priority_levels", "2,3,7,99,abc"
        )

        high_priority_levels = self.env["helpdesk.ticket"]._get_high_priority_levels()
        valid_priorities = dict(
            self.env["helpdesk.ticket"]._fields["priority"].selection
        ).keys()

        for level in high_priority_levels:
            self.assertIn(level, valid_priorities)

        self.assertIn("2", high_priority_levels)
        self.assertIn("3", high_priority_levels)
        self.assertNotIn("7", valid_priorities)
        self.assertNotIn("7", high_priority_levels)
        self.assertNotIn("99", valid_priorities)
        self.assertNotIn("99", high_priority_levels)
        self.assertNotIn("abc", valid_priorities)
        self.assertNotIn("abc", high_priority_levels)
