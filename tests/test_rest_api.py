import unittest
import requests


class TestRESTAPIService(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://localhost:5000/api'

    def test_generate(self):
        response = requests.post(f'{self.base_url}/generate', json={'user_id': 'test_user', 'metadata': {'age': 25}})
        self.assertEqual(response.status_code, 200)
        self.assertIn('image_path', response.json())

    def test_get_interactions(self):
        response = requests.get(f'{self.base_url}/interactions/test_user')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()