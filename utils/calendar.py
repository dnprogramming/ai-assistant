from config import Config
from datetime import timedelta
from dateutil import parser

class calendar:
    def extract_meeting_info(email_data):
        host = email_data['from']
        recipients = email_data['to']
        try:
            date_time_str = email_data['snippet'].split('at')[1].strip()
            meeting_time = parser.parse(date_time_str, fuzzy=True)
        except ValueError:
            print("Failed to parse date/time from email.")
            return None, None, None
        return host, recipients, meeting_time

    def create_meeting_event(service, host, recipients, meeting_time, summary="Meeting"):
        """Creates a meeting event in Google Calendar."""
        event = {
            'summary': summary,
            'start': {
                'dateTime': meeting_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Chicago'
            },
            'end': {
                'dateTime': (meeting_time + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'America/Chicago'
            },
            'attendees': [
                {'email': host},
                *[{'email': recipient} for recipient in recipients]
            ]
        }
        event = service.events().insert(calendarId='primary', body=event).execute()