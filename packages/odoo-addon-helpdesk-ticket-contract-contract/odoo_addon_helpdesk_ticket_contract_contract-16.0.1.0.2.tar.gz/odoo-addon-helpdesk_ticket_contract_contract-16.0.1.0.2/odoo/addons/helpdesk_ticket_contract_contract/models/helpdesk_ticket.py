from odoo import models, api, fields
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    contract_id = fields.Many2one(comodel_name="contract.contract", string="Contract")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("contract_id"):
                continue
            contract = self.env["contract.contract"].browse(vals["contract_id"])
            if contract and not vals.get("partner_id"):
                vals["partner_id"] = contract.partner_id.id
                continue
            if vals["partner_id"] != contract.partner_id.id:
                msg = """
                    Cannot create ticket with contract {}, which has a different
                    partner than the one indicated in 'partner_id' param ({})
                """.format(
                    vals["contract_id"], vals["partner_id"]
                )
                raise ValidationError(msg)
        return super().create(vals_list)
