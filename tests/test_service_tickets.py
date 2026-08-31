from application import create_app
from application.extensions import db
from application.models import Customer, Mechanic, Inventory, ServiceTicket
from config import TestingConfig
import unittest


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            self.customer = Customer(name='test_customer', email='cust@email.com', phone='111-111-1111', password='test')
            self.mechanic = Mechanic(name='test_mechanic', email='mech@email.com', phone='222-222-2222', salary=50000)
            self.part = Inventory(name='Brake Pad', price=49.99)
            db.session.add_all([self.customer, self.mechanic, self.part])
            db.session.commit()

            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.part_id = self.part.id

            self.ticket = ServiceTicket(VIN='1FTFW1E58MFA00001', service_date='2026-01-01', service_desc='Oil change', customer_id=self.customer_id)
            db.session.add(self.ticket)
            db.session.commit()
            self.ticket_id = self.ticket.id

        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        payload = {'VIN': '2FTFW1E58MFA00002', 'service_date': '2026-02-01', 'service_desc': 'Brake check', 'customer_id': self.customer_id}
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], '2FTFW1E58MFA00002')

    def test_invalid_creation(self):
        payload = {'service_date': '2026-02-01', 'service_desc': 'Brake check', 'customer_id': self.customer_id}
        response = self.client.post('/service-tickets/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['VIN'], ['Missing data for required field.'])

    def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_assign_mechanic(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            ticket = db.session.get(ServiceTicket, self.ticket_id)
            self.assertIn(self.mechanic_id, [m.id for m in ticket.mechanics])

    def test_assign_mechanic_already_assigned(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 400)

    def test_remove_mechanic(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/assign-mechanic/{self.mechanic_id}')
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            ticket = db.session.get(ServiceTicket, self.ticket_id)
            self.assertNotIn(self.mechanic_id, [m.id for m in ticket.mechanics])

    def test_remove_mechanic_not_assigned(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/remove-mechanic/{self.mechanic_id}')
        self.assertEqual(response.status_code, 400)

    def test_edit_ticket(self):
        payload = {'add_ids': [self.mechanic_id], 'remove_ids': []}
        response = self.client.put(f'/service-tickets/{self.ticket_id}/edit', json=payload)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            ticket = db.session.get(ServiceTicket, self.ticket_id)
            self.assertIn(self.mechanic_id, [m.id for m in ticket.mechanics])

    def test_add_part(self):
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            ticket = db.session.get(ServiceTicket, self.ticket_id)
            self.assertIn(self.part_id, [p.id for p in ticket.parts])

    def test_add_part_already_added(self):
        self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        response = self.client.put(f'/service-tickets/{self.ticket_id}/add-part/{self.part_id}')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()