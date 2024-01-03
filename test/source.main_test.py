import unittest
from unittest.mock import patch, MagicMock
from source.main import Main


class TestMain(unittest.TestCase):

    @patch("source.main.config.Config")
    @patch("source.main.calendar.calendar")
    def setUp(self, mock_calendar, mock_config):
        mock_config.return_value.email_to_listen_for = "test_email"
        mock_calendar.return_value.scheduleMeeting = MagicMock()
        mock_calendar.return_value.sendDailyMeetingsEmail = MagicMock()
        self.main = Main()

    def tearDown(self):
        del self.main

    def test_init(self):
        self.assertEqual(self.main.target_email, "test_email")
        self.assertFalse(self.main.sent_daily_meetings_email)


if __name__ == "__main__":
    unittest.main()
