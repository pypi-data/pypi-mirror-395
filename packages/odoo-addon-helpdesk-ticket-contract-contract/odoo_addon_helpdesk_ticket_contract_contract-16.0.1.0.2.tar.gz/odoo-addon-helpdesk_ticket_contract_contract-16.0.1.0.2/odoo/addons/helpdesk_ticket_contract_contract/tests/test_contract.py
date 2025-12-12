from odoo.tests import common, tagged


@tagged("post_install", "-at_install", "helpdesk_ticket_contract_contract")
class TestContractContract(common.TransactionCase):
    def test_contract_helpdesk_ticket_count(self):
        ticket_1 = self.env.ref("helpdesk_mgmt.helpdesk_ticket_1")
        ticket_2 = self.env.ref("helpdesk_mgmt.helpdesk_ticket_2")
        ticket_7 = self.env.ref("helpdesk_mgmt.helpdesk_ticket_7")

        self.assertFalse(ticket_1.stage_id.closed)
        self.assertFalse(ticket_2.stage_id.closed)
        self.assertTrue(ticket_7.stage_id.closed)

        contract = self.env["contract.contract"].create(
            {
                "name": "Contract with tickets",
                "partner_id": ticket_1.partner_id.id,
            }
        )

        self.assertFalse(contract.helpdesk_ticket_ids)
        self.assertEqual(contract.helpdesk_ticket_count, 0)
        self.assertEqual(contract.helpdesk_ticket_active_count, 0)
        self.assertEqual(contract.helpdesk_ticket_count_string, "0 / 0")

        # Assign tickets to contract
        contract.helpdesk_ticket_ids = [(6, 0, [ticket_1.id, ticket_2.id, ticket_7.id])]

        self.assertIn(ticket_1, contract.helpdesk_ticket_ids)
        self.assertIn(ticket_2, contract.helpdesk_ticket_ids)
        self.assertIn(ticket_7, contract.helpdesk_ticket_ids)
        self.assertEqual(contract.helpdesk_ticket_count, 3)
        self.assertEqual(contract.helpdesk_ticket_active_count, 2)
        self.assertEqual(contract.helpdesk_ticket_count_string, "2 / 3")
