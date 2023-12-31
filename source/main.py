import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import config
from time import sleep
from utils import gmail as service
import os.path


ASSISTANT_SERVICE_ACCOUNT_INFO = config.Config().assistant_credentials
MAIN_SERVICE_ACCOUNT_INFO = config.Config().main_credentials

ASSISTANT_SCOPES = [config.Config().assistant_scopes]
MAIN_SCOPES = [config.Config().main_scopes]


class Main:

    def __init__(self):
        self.target_email = config.Config().email_to_listen_for

    def scheduleMeeting(self, meeting):
        email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"

        # Find all email matches
        attendees = re.findall(email_pattern, meeting)

        print(attendees)

        # event = {
        #     "summary": "Your meeting title",
        #     "description": "Meeting description",
        #     "start": {
        #         "dateTime": "2024-01-01T10:00:00-07:00"
        #     },
        #     "end": {
        #         "dateTime": "2024-01-01T11:00:00-07:00"
        #     },
        #     "attendees": [
        #         {"email": email} for email in attendees
        #     ]
        # }

# Send meeting invites
    #service.events().insert(calendarId="primary", body=event).execute()
        

    def main(self):
        while True:
            creds = None
            service = None
            if os.path.exists("assistant_token.json"):
                creds = Credentials.from_authorized_user_file(
                    "assistant_token.json", ASSISTANT_SCOPES
                )
                service = build("gmail", "v1", credentials=creds)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        ASSISTANT_SERVICE_ACCOUNT_INFO, ASSISTANT_SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    with open("assistant_token.json", "w") as token:
                        token.write(creds.to_json())

                    service = build("gmail", "v1", credentials=creds)
                    print(service)
            results = (
                service.users()
                .messages()
                .list(userId="me", q=f"from:{self.target_email}")
                .execute()
            )
            messages = results.get("messages", [])

            if messages:
                for message in messages:
                    message = (
                        service.users()
                        .messages()
                        .get(userId="me", id=message["id"])
                        .execute()
                    )
                    if "UNREAD" in message["labelIds"]:
                        messagedata = service.users().messages().get(userId="me", id=message["id"]).execute()
                        payload = messagedata["snippet"]
                        print(messagedata)
                        
                        service.users().messages().modify(
                            userId="me",
                            id=message["id"],
                            body={"removeLabelIds": ["UNREAD"]},
                        ).execute()
                        message = MIMEText("I am working on your request now.")
                        message["to"] = self.target_email
                        message["subject"] = "Received Request."
                        create_message = {
                            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode()
                        }

                        try:
                            message = (
                                service.users()
                                .messages()
                                .send(userId="me", body=create_message)
                                .execute()
                            )
                        except HttpError as error:
                            print(f"An error occurred: {error}")
                            message = None
            sleep(60)
