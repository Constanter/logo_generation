import unittest
from unittest.mock import patch
from logo_generation.ml_model_service.src.main import image_generator, store_image_path_in_database
from logo_generation.ml_model_service.src.utils import generate_prompt, generate_negative_prompt


class TestMLModelService(unittest.TestCase):
    @patch('logo_generation.ml_model_service.src.main.txt2img_model')
    def test_image_generator(self, mock_txt2img):
        mock_txt2img.return_value.images = ['mock_image.png']
        metadata = {'age': 25}

        image_bytes, returned_metadata = image_generator('mock_path', metadata)

        self.assertIsNotNone(image_bytes)
        self.assertEqual(returned_metadata, metadata)

    def test_generate_prompt(self):
        prompt = generate_prompt(age=25)
        self.assertIn("engaging in", prompt)

    def test_generate_negative_prompt(self):
        negative_prompt = generate_negative_prompt()
        self.assertIn("avoid the pitfalls", negative_prompt)

    @patch('psycopg2.connect')
    def test_store_image_path_in_database(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        store_image_path_in_database('test_user', 'test_path', {})

        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()