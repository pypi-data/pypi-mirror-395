import unittest
from unittest.mock import patch, MagicMock
from acs_chatbot.core import get_response, summarize_text, format_response, configure_api_key

class TestACSChatbot(unittest.TestCase):
    
    @patch('acs_chatbot.core.genai')
    def test_configure_api_key(self, mock_genai):
        configure_api_key("test_key")
        mock_genai.configure.assert_called_with(api_key="test_key")

    @patch('acs_chatbot.core.genai')
    def test_get_response(self, mock_genai):
        # Mock the model and response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Mocked AI Response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        response = get_response("Hello")
        self.assertEqual(response, "Mocked AI Response")
        mock_genai.GenerativeModel.assert_called_with("gemini-pro")

    @patch('acs_chatbot.core.get_response')
    def test_summarize_text(self, mock_get_response):
        mock_get_response.return_value = "Summary"
        summary = summarize_text("Long text")
        self.assertEqual(summary, "Summary")
        mock_get_response.assert_called()

    def test_format_response(self):
        raw = "  hello world  "
        formatted = format_response(raw)
        self.assertEqual(formatted, "hello world")
        
        self.assertEqual(format_response(""), "")

if __name__ == '__main__':
    unittest.main()
