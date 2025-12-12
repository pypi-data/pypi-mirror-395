{
    "version": "16.0.1.0.0",
    "name": "Helpdesk Priority Filter",
    "depends": [
        "helpdesk_mgmt",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Customer Relationship Management",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Adds a configurable field to set the helpdesk ticket priority
        levels considered high priority.
    """,
    "data": [
        "views/helpdesk_ticket_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "demo": [],
    "application": False,
    "installable": True,
}
