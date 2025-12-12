import unittest
from unittest.mock import patch, MagicMock
from ai_assist_utils.core import get_response, summarize_text, format_response

class TestAIAssistUtils(unittest.TestCase):

    def test_format_response(self):
        """Test that format_response cleans text correctly."""
        raw = "  Hello World  "
        expected = "Hello World"
        self.assertEqual(format_response(raw), expected)

        self.assertEqual(format_response(None), "")

    @patch('ai_assist_utils.core.openai.OpenAI')
    def test_get_response_success(self, mock_openai):
        """Test get_response with a successful API call."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Paris"
        mock_client.chat.completions.create.return_value = mock_completion

        # Call function
        response = get_response("What is the capital of France?", api_key="fake-key")
        
        # Assertions
        self.assertEqual(response, "Paris")
        mock_client.chat.completions.create.assert_called_once()

    @patch('ai_assist_utils.core.openai.OpenAI')
    def test_summarize_text(self, mock_openai):
        """Test summarize_text calls get_response correctly."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Summary"
        mock_client.chat.completions.create.return_value = mock_completion

        # Call function
        summary = summarize_text("Long text", api_key="fake-key")
        
        # Assertions
        self.assertEqual(summary, "Summary")
        # Check if the prompt was constructed correctly in the call
        call_args = mock_client.chat.completions.create.call_args
        self.assertIn("Please summarize the following text", call_args[1]['messages'][0]['content'])

if __name__ == '__main__':
    unittest.main()
