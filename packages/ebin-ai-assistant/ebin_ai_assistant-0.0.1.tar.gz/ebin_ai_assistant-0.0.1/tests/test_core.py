import unittest
from unittest.mock import patch, MagicMock
from ebin_ai_assistant.core import get_response, summarize_text, format_response, configure_api

class TestAIHelper(unittest.TestCase):
    def setUp(self):
        configure_api("fake_key")

    @patch('ebin_ai_assistant.core.genai.GenerativeModel')
    def test_get_response(self, mock_model_class):
        # Setup mock
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "AI Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        prompt = "Hello"
        response = get_response(prompt)
        
        self.assertEqual(response, "AI Response")
        mock_model.generate_content.assert_called_with(prompt)

    @patch('ebin_ai_assistant.core.get_response')
    def test_summarize_text(self, mock_get_response):
        mock_get_response.return_value = "Summary text"
        
        text = "Long text"
        summary = summarize_text(text)
        
        self.assertEqual(summary, "Summary text")
        mock_get_response.assert_called_once()
        args, _ = mock_get_response.call_args
        self.assertIn("summarize", args[0])
        self.assertIn(text, args[0])

    @patch('ebin_ai_assistant.core.get_response')
    def test_format_response(self, mock_get_response):
        mock_get_response.return_value = "Formatted text"
        
        raw_text = "  Hello   \n\n World  "
        formatted = format_response(raw_text)
        
        self.assertEqual(formatted, "Formatted text")
        mock_get_response.assert_called_once()
        args, _ = mock_get_response.call_args
        self.assertIn("format", args[0])
        self.assertIn(raw_text, args[0])

if __name__ == '__main__':
    unittest.main()
