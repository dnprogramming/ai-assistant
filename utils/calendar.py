import base64
import pytz
import re
from email.mime.text import MIMEText
from requests import HTTPError
from config import config
from utils import gemini
from datetime import datetime, timedelta
from googleapiclient.discovery import build


class calendar:

    def __init__(self):
        self.target_emails = config.Config().emails_to_listen_for

    def sendDailyMeetingsEmail(self, main_creds, assistant_service):
        service = build("calendar", "v3", credentials=main_creds)
        today = datetime.today()
        start = (
            datetime(today.year, today.month, today.day, 00, 00)
        ).isoformat() + "Z"
        tomorrow = today + datetime.timedelta(days=1)
        end = (
            datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00)
        ).isoformat() + "Z"
        events_results = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        message = MIMEText(events_results.get("items", []))
        message["to"] = self.target_emails[0]
        message["subject"] = "Your Schedule for Today."
        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
        try:
            message = (
                assistant_service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
        except HTTPError as error:
            print(f"An error occurred: {error}")
            message = None

    def scheduleMeeting(self, meetinginfo, main_creds):
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
        attendees = re.findall(email_pattern, meetinginfo)
        result = gemini.gemini.generate_text(meetinginfo)
        results = result.split("|")
        event = {
            "summary": results[0],
            "description": results[1],
            "start": {
                "dateTime": datetime.isoformat(
                    datetime.fromisoformat(
                        results[2].replace("Date: ", "").replace(" ", "")
                    ).astimezone(pytz.timezone("US/Central"))
                ),
                "timeZone": "America/Chicago",
            },
            "end": {
                "dateTime": datetime.isoformat(
                    datetime.fromisoformat(
                        results[2].replace("Date: ", "").replace(" ", "")
                    ).astimezone(pytz.timezone("US/Central"))
                    + timedelta(minutes=60)
                ),
                "timeZone": "America/Chicago",
            },
            "attendees": [{"email": email} for email in attendees],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }
        service = build("calendar", "v3", credentials=main_creds)
        service.events().insert(
            calendarId="primary", body=event, sendUpdates="all"
        ).execute()
