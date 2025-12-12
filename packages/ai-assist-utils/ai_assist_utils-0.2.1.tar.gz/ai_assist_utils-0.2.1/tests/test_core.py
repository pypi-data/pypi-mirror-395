import unittest
from unittest.mock import patch, MagicMock
from ai_assist_utils.core import get_response, summarize_text, format_response

class TestAIAssistUtils(unittest.TestCase):

    def test_format_response(self):
        """Test that format_response cleans text correctly."""
        raw = "  Hello World  "
        expected = "Hello World"
        self.assertEqual(format_response(raw), expected)

    @patch('ai_assist_utils.core.genai')
    def test_get_response_success(self, mock_genai):
        """Test get_response with a successful API call."""
        # Setup mock
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Gemini Response"
        mock_model.generate_content.return_value = mock_response

        # Call function
        response = get_response("Hello", api_key="fake-key")
        
        # Assertions
        self.assertEqual(response, "Gemini Response")
        mock_genai.configure.assert_called_with(api_key="fake-key")
        mock_model.generate_content.assert_called_with("Hello")

if __name__ == '__main__':
    unittest.main()
