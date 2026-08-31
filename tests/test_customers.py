from application import create_app
from application.extensions import db
from application.models import Customer
from application.utils.util import encode_token
from config import TestingConfig
import unittest


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.customer = Customer(name='test_user', email='test@email.com', phone='555-555-5555', password='test')
            db.session.add(self.customer)
            db.session.commit()
            self.customer_id = self.customer.id
            self.token = encode_token(self.customer_id)
        self.client = self.app.test_client()

    def test_create_customer(self):
        payload = {
            'name': 'John Doe',
            'email': 'jd@email.com',
            'phone': '123-456-7890',
            'password': '123'
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_invalid_creation(self):
        payload = {
            'name': 'John Doe',
            'phone': '123-456-7890',
            'password': '123'
        }
        response = self.client.post('/customers/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_login_customer(self):
        credentials = {'email': 'test@email.com', 'password': 'test'}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    def test_invalid_login(self):
        credentials = {'email': 'test@email.com', 'password': 'wrong_password'}
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid email or password')

    def test_update_customer(self):
        payload = {
            'name': 'Updated Name',
            'email': 'test@email.com',
            'phone': '555-555-5555',
            'password': 'test'
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put('/customers/', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_delete_customer(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        
    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['customers']), 1)

    def test_get_customer(self):
        response = self.client.get(f'/customers/{self.customer_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/9999')
        self.assertEqual(response.status_code, 404)

    def test_my_tickets(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


if __name__ == '__main__':
    unittest.main()