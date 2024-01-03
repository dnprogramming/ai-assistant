import unittest
from unittest.mock import patch, MagicMock
from utils import gemini


class TestGemini(unittest.TestCase):

    @patch("utils.gemini.config.Config")
    @patch("utils.gemini.genai.GenerativeModel")
    def setUp(self, mock_model, mock_config):
        mock_config.return_value.gemini_api_key = "test_key"
        self.mock_model = mock_model
        self.gemini = gemini.gemini

    def tearDown(self):
        del self.gemini

    def test_generate_text(self):
        mock_response = MagicMock()
        mock_response.text = "•test_text•"
        self.mock_model.return_value.generate_content.return_value = mock_response
        result = self.gemini.generate_text("test_prompt")
        self.assertEqual(result, "test_text")
        self.mock_model.return_value.generate_content.assert_called_once_with(
            "Please get the description, subject, and date as a datetime in iso format for the meeting. The date in the email will be in mm-dd-yyyy format and please separate each of the three fields with a pipe character like this format: subject|description|date. The email states: test_prompt"
        )

    def test_translate(self):
        mock_response = MagicMock()
        mock_response.text = "test_text"
        self.mock_model.return_value.generate_content.return_value = mock_response
        result = self.gemini.translate("test_prompt")
        self.assertEqual(result, "test_text")
        self.mock_model.return_value.generate_content.assert_called_once_with(
            "test_prompt"
        )

    def test_question(self):
        mock_response = MagicMock()
        mock_response.text = "test_text"
        self.mock_model.return_value.generate_content.return_value = mock_response
        result = self.gemini.question("test_prompt")
        self.assertEqual(result, "test_text")
        self.mock_model.return_value.generate_content.assert_called_once_with(
            "test_prompt"
        )


if __name__ == "__main__":
    unittest.main()
