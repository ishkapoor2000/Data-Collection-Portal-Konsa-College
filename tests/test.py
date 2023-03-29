'''
python -m unittest discover tests
'''
import unittest
from flask import Flask, url_for

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

    def test_dashboard(self):
        with self.app.test_client() as client:
            response = client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'dashboard page', response.data)

    def test_index(self):
        with self.app.test_client() as client:
            response = client.get('/index')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'index page', response.data)

    def test_login_page(self):
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)

    def test_login(self):
        with self.app.test_client() as client:
            response = client.post('/', data=dict(
                username='kcadmin123',
                password='kc1234'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome, tester admin!', response.data)

    # def test_logout(self):
    #     with self.app.test_client() as client:
    #         response = client.get('/logout', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'You have been logged out', response.data)

    def test_url_for(self):
        with self.app.test_request_context():
            self.assertEqual(url_for('dashboard'), '/dashboard')
            self.assertEqual(url_for('login'), '/')
            self.assertEqual(url_for('index'), '/index')

if __name__ == '__main__':
    unittest.main()
