import unittest
from unittest.mock import patch, MagicMock
from ai_assistant_lib.core import get_response, summarize_text, format_response

class TestAIAssistant(unittest.TestCase):

    @patch('ai_assistant_lib.core.genai')
    def test_get_response(self, mock_genai):
        # Mock the GenerativeModel and its generate_content method
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a mock response."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        response = get_response("Hello", api_key="test_key")
        self.assertEqual(response, "This is a mock response.")
        mock_genai.configure.assert_called_with(api_key="test_key")

    def test_format_response(self):
        # Test markdown to HTML conversion
        markdown_text = "**Hello**"
        expected_html = "<p><strong>Hello</strong></p>"
        self.assertEqual(format_response(markdown_text), expected_html)

    @patch('ai_assistant_lib.core.get_response')
    def test_summarize_text(self, mock_get_response):
        mock_get_response.return_value = "Summary"
        response = summarize_text("Long text", api_key="test_key")
        self.assertEqual(response, "Summary")
        mock_get_response.assert_called()

if __name__ == '__main__':
    unittest.main()
