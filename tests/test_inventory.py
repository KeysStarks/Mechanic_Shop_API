from application import create_app
from application.extensions import db
from application.models import Inventory
from config import TestingConfig
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.part = Inventory(name='Brake Pad', price=49.99)
            db.session.add(self.part)
            db.session.commit()
            self.part_id = self.part.id
        self.client = self.app.test_client()

    def test_create_part(self):
        payload = {'name': 'Oil Filter', 'price': 12.99}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Oil Filter')

    def test_invalid_creation(self):
        payload = {'name': 'Oil Filter'}
        response = self.client.post('/inventory/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])

    def test_get_parts(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_get_part(self):
        response = self.client.get(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Brake Pad')

    def test_get_part_not_found(self):
        response = self.client.get('/inventory/9999')
        self.assertEqual(response.status_code, 404)

    def test_update_part(self):
        payload = {'name': 'Brake Pad Deluxe', 'price': 59.99}
        response = self.client.put(f'/inventory/{self.part_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Brake Pad Deluxe')

    def test_update_part_not_found(self):
        payload = {'name': 'Brake Pad Deluxe', 'price': 59.99}
        response = self.client.put('/inventory/9999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_part(self):
        response = self.client.delete(f'/inventory/{self.part_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_part_not_found(self):
        response = self.client.delete('/inventory/9999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()