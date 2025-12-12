# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "version": "16.0.1.0.2",
    "name": "Helpdesk ticket linked with contract contract",
    "depends": [
        "helpdesk_mgmt",
        "contract",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Auth",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Allows to link helpdesk tickets with contracts.
    """,
    "data": ["views/contract_contract.xml", "views/helpdesk_ticket.xml"],
    "demo": [],
    "application": False,
    "installable": True,
}
