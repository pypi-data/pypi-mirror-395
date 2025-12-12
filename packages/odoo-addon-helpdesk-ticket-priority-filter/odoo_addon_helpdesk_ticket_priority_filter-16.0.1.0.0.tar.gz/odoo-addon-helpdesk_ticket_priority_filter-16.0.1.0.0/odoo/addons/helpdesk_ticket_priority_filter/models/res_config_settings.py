from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    high_priority_levels = fields.Char(
        string="High priority tickets",
        config_parameter="helpdesk_ticket_priority_filter.high_priority_levels",
        default="2,3",
        help="Values separated by commas (e.g., 2,3)",
    )
