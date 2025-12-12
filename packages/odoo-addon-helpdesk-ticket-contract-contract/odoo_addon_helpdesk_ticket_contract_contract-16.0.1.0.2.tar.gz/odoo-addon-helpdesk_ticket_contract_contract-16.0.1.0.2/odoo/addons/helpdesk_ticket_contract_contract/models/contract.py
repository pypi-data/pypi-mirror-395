from odoo import models, api, fields


class Contract(models.Model):
    _inherit = "contract.contract"

    helpdesk_ticket_ids = fields.One2many(
        comodel_name="helpdesk.ticket",
        inverse_name="contract_id",
        string="Related tickets",
    )

    helpdesk_ticket_count = fields.Integer(
        compute="_compute_helpdesk_ticket_count", string="Ticket count"
    )

    helpdesk_ticket_active_count = fields.Integer(
        compute="_compute_helpdesk_ticket_count", string="Ticket active count"
    )

    helpdesk_ticket_count_string = fields.Char(
        compute="_compute_helpdesk_ticket_count", string="Tickets"
    )

    @api.depends("helpdesk_ticket_ids")
    def _compute_helpdesk_ticket_count(self):
        for record in self:
            record.helpdesk_ticket_count = (
                record.helpdesk_ticket_ids and len(record.helpdesk_ticket_ids) or 0
            )
            active_tickets = record.helpdesk_ticket_ids.filtered(
                lambda t: not t.stage_id.closed
            )
            record.helpdesk_ticket_active_count = (
                active_tickets and len(active_tickets) or 0
            )
            record.helpdesk_ticket_count_string = "{} / {}".format(
                record.helpdesk_ticket_active_count, record.helpdesk_ticket_count
            )

    def action_view_helpdesk_tickets(self):
        return {
            "name": self.name,
            "view_mode": "tree,form",
            "res_model": "helpdesk.ticket",
            "type": "ir.actions.act_window",
            "domain": [("contract_id", "=", self.id)],
            "context": {
                "search_default_open": True,
                "default_partner_id": self.partner_id.id if self.partner_id else False,
                "default_contract_id": self.id
            },
        }
