import os
import unittest
from unittest.mock import patch
from config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def tearDown(self):
        del self.config

    @patch.dict(
        os.environ,
        {
            "CREDENTIALS": "test_credentials",
            "ASSISTANT_SCOPES": "test_scopes",
            "GEMINI_API_KEY": "test_key",
            "EMAIL_TO_LISTEN_FOR": "test_email",
            "MAIN_SCOPES": "test_main_scopes",
        },
    )
    def test_config(self):
        self.assertEqual(self.config.credentials, "test_credentials")
        self.assertEqual(self.config.assistant_scopes, "test_scopes")
        self.assertEqual(self.config.gemini_api_key, "test_key")
        self.assertEqual(self.config.email_to_listen_for, "test_email")
        self.assertEqual(self.config.main_scopes, "test_main_scopes")


if __name__ == "__main__":
    unittest.main()
