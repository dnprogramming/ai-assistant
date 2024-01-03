import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from googleapiclient.discovery import Resource
from email.mime.text import MIMEText
from requests import HTTPError
from utils import calendar


class TestCalendar(unittest.TestCase):

    def setUp(self):
        self.calendar = calendar.calendar()
        self.main_creds = MagicMock()
        self.assistant_service = MagicMock()

    def test_sendDailyMeetingsEmail(self):
        # Mock the build function
        build_mock = MagicMock()
        build_mock.return_value = Resource(self.main_creds)
        calendar.build = build_mock

        # Mock the events list response
        events_list_mock = MagicMock()
        events_list_mock.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "Meeting 1",
                    "start": {"dateTime": "2022-01-01T10:00:00Z"},
                    "end": {"dateTime": "2022-01-01T11:00:00Z"},
                },
                {
                    "summary": "Meeting 2",
                    "start": {"dateTime": "2022-01-01T14:00:00Z"},
                    "end": {"dateTime": "2022-01-01T15:00:00Z"},
                },
            ]
        }
        self.calendar.service.events().list = events_list_mock

        # Mock the MIMEText object
        mime_text_mock = MagicMock()
        MIMEText_mock = MagicMock(return_value=mime_text_mock)
        calendar.MIMEText = MIMEText_mock

        # Mock the assistant_service messages send response
        messages_send_mock = MagicMock()
        self.assistant_service.users().messages().send = messages_send_mock

        # Call the method
        self.calendar.sendDailyMeetingsEmail(self.main_creds, self.assistant_service)

        # Assertions
        build_mock.assert_called_once_with(
            "calendar", "v3", credentials=self.main_creds
        )
        events_list_mock.assert_called_once_with(
            calendarId="primary",
            timeMin=datetime.now().replace(hour=0, minute=0, second=0).isoformat()
            + "Z",
            timeMax=(datetime.now() + timedelta(days=1))
            .replace(hour=0, minute=0, second=0)
            .isoformat()
            + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        MIMEText_mock.assert_called_once_with(
            '[{"summary": "Meeting 1", "start": {"dateTime": "2022-01-01T10:00:00Z"}, "end": {"dateTime": "2022-01-01T11:00:00Z"}}, {"summary": "Meeting 2", "start": {"dateTime": "2022-01-01T14:00:00Z"}, "end": {"dateTime": "2022-01-01T15:00:00Z"}}]'
        )
        messages_send_mock.assert_called_once_with(
            userId="me",
            body={"raw": "base64_encoded_message"},
        )

    def test_scheduleMeeting(self):
        # Mock the gemini.gemini.generate_text function
        generate_text_mock = MagicMock()
        generate_text_mock.return_value = (
            "Meeting Summary | Meeting Description | Date: 2022-01-01 10:00:00"
        )
        calendar.gemini.gemini.generate_text = generate_text_mock

        # Mock the build function
        build_mock = MagicMock()
        build_mock.return_value = Resource(self.main_creds)
        calendar.build = build_mock

        # Mock the events insert response
        events_insert_mock = MagicMock()
        self.calendar.service.events().insert = events_insert_mock

        # Call the method
        self.calendar.scheduleMeeting("Meeting info", self.main_creds)

        # Assertions
        generate_text_mock.assert_called_once_with("Meeting info")
        build_mock.assert_called_once_with(
            "calendar", "v3", credentials=self.main_creds
        )
        events_insert_mock.assert_called_once_with(
            calendarId="primary",
            body={
                "summary": "Meeting Summary",
                "description": "Meeting Description",
                "start": {
                    "dateTime": "2022-01-01T10:00:00-06:00",
                    "timeZone": "America/Chicago",
                },
                "end": {
                    "dateTime": "2022-01-01T11:00:00-06:00",
                    "timeZone": "America/Chicago",
                },
                "attendees": [{"email": "attendee@example.com"}],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 24 * 60},
                        {"method": "popup", "minutes": 10},
                    ],
                },
            },
            sendUpdates="all",
        )


if __name__ == "__main__":
    unittest.main()
