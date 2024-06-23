import unittest
from unittest.mock import patch
from logo_generation.storage_service.src.db import store_interaction, get_marked_images


class TestStorageService(unittest.TestCase):
    @patch('psycopg2.connect')
    def test_store_interaction(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        store_interaction('test_user', 'test_path', '{}')

        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_marked_images(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [('test_user', 'test_path', True)]

        marked_images = get_marked_images()

        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        self.assertEqual(marked_images, [('test_user', 'test_path', True)])

if __name__ == '__main__':
    unittest.main()
