from application import create_app
from application.extensions import db
from application.models import Mechanic
from config import TestingConfig
import unittest


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.mechanic = Mechanic(name='test_mechanic', email='mech@email.com', phone='111-111-1111', salary=50000)
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        payload = {'name': 'Jane Wrench', 'email': 'jane@email.com', 'phone': '222-222-2222', 'salary': 55000}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Jane Wrench')

    def test_invalid_creation(self):
        payload = {'name': 'Jane Wrench', 'phone': '222-222-2222', 'salary': 55000}
        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_mechanic(self):
        payload = {'name': 'Updated Name', 'email': 'mech@email.com', 'phone': '111-111-1111', 'salary': 60000}
        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Name')

    def test_update_mechanic_not_found(self):
        payload = {'name': 'Updated Name', 'email': 'mech@email.com', 'phone': '111-111-1111', 'salary': 60000}
        response = self.client.put('/mechanics/9999', json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/9999')
        self.assertEqual(response.status_code, 404)

    def test_most_active_mechanics(self):
        response = self.client.get('/mechanics/most-active')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)


if __name__ == '__main__':
    unittest.main()