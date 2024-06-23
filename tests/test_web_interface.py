import unittest
import gradio as gr
from logo_generation.web_interface_service.src.interface import generate_image, mark_image


class TestWebInterfaceService(unittest.TestCase):
    def test_generate_image(self):
        img = generate_image('test_user', {'age': 25})
        self.assertIsInstance(img, gr.outputs.Image)

    def test_mark_image(self):
        result = mark_image('test_user', True)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()