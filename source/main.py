import base64
import os.path
import pytz
from datetime import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import calendar
from utils import gemini
from config import config
from time import sleep


ACCOUNT_INFO = config.Config().credentials
ASSISTANT_SCOPES = [config.Config().assistant_scopes]
MAIN_SCOPES = [config.Config().main_scopes]


class Main:

    def __init__(self):
        self.target_email = config.Config().email_to_listen_for
        self.scheduleMeeting = calendar.calendar().scheduleMeeting
        self.sendDailyMeetingsEmail = calendar.calendar().sendDailyMeetingsEmail
        self.sent_daily_meetings_email = False

    def main(self):
        assistant_creds = None
        assistant_service = None
        main_creds = None
        while True:
            if os.path.exists("assistant_token.json"):
                assistant_creds = Credentials.from_authorized_user_file(
                    "assistant_token.json", ASSISTANT_SCOPES
                )
                assistant_service = build("gmail", "v1", credentials=assistant_creds)
            if not assistant_creds or not assistant_creds.valid:
                if (
                    assistant_creds
                    and assistant_creds.expired
                    and assistant_creds.refresh_token
                ):
                    assistant_creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        ACCOUNT_INFO, ASSISTANT_SCOPES
                    )
                    assistant_creds = flow.run_local_server(bind_addr="0.0.0.0", port=0)
                    with open("assistant_token.json", "w") as token:
                        token.write(assistant_creds.to_json())

                    assistant_service = build(
                        "gmail", "v1", credentials=assistant_creds
                    )
            if os.path.exists("main_token.json"):
                main_creds = Credentials.from_authorized_user_file(
                    "main_token.json", MAIN_SCOPES
                )
            if not main_creds or not main_creds.valid:
                if main_creds and main_creds.expired and main_creds.refresh_token:
                    main_creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        ACCOUNT_INFO, MAIN_SCOPES
                    )
                    main_creds = flow.run_local_server(bind_addr="0.0.0.0", port=0)
                    with open("main_token.json", "w") as token:
                        token.write(main_creds.to_json())
            results = (
                assistant_service.users()
                .messages()
                .list(userId="me", q=f"from:{self.target_email}")
                .execute()
            )
            messages = results.get("messages", [])
            if (
                datetime.now().astimezone(pytz.timezone("US/Central")).hour == 4
                and self.sent_daily_meetings_email == True
            ):
                self.sent_daily_meetings_email = False
            if (
                datetime.now().astimezone(pytz.timezone("US/Central")).hour == 6
                and self.sent_daily_meetings_email == False
            ):
                self.sendDailyMeetingsEmail(main_creds, assistant_service)
                self.sent_daily_meetings_email = True
            if messages:
                for message in messages:
                    message = (
                        assistant_service.users()
                        .messages()
                        .get(userId="me", id=message["id"])
                        .execute()
                    )
                    if "UNREAD" in message["labelIds"]:
                        messagedata = (
                            assistant_service.users()
                            .messages()
                            .get(userId="me", id=message["id"])
                            .execute()
                        )
                        assistant_service.users().messages().modify(
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
                                assistant_service.users()
                                .messages()
                                .send(userId="me", body=create_message)
                                .execute()
                            )
                        except HttpError as error:
                            print(f"An error occurred: {error}")
                            message = None

                        try:
                            emailreasoning = None
                            for header in messagedata["payload"]["headers"]:
                                if header["name"] == "Subject":
                                    emailreasoning = header["value"].lower()
                            if "meeting" in emailreasoning:
                                body = messagedata["payload"]["parts"][0]["body"]
                                entire_body = base64.urlsafe_b64decode(
                                    body["data"].encode("ASCII")
                                ).decode("utf-8")
                                payload = entire_body
                                self.scheduleMeeting(payload, main_creds)
                            elif "translate" in emailreasoning:
                                body = messagedata["payload"]["parts"][0]["body"]
                                entire_body = base64.urlsafe_b64decode(
                                    body["data"].encode("ASCII")
                                ).decode("utf-8")
                                payload = entire_body
                                result = gemini.gemini.translate(payload)
                                message = MIMEText(result)
                                message["to"] = self.target_email
                                message["subject"] = "Translation you requested"
                                create_message = {
                                    "raw": base64.urlsafe_b64encode(
                                        message.as_bytes()
                                    ).decode()
                                }
                                try:
                                    message = (
                                        assistant_service.users()
                                        .messages()
                                        .send(userId="me", body=create_message)
                                        .execute()
                                    )
                                except HttpError as error:
                                    print(f"An error occurred: {error}")
                                    message = None
                            else:
                                body = messagedata["payload"]["parts"][0]["body"]
                                entire_body = base64.urlsafe_b64decode(
                                    body["data"].encode("ASCII")
                                ).decode("utf-8")
                                payload = entire_body
                                result = gemini.gemini.question(payload)
                                message = MIMEText(result)
                                message["to"] = self.target_email
                                message["subject"] = "Answer to your question"
                                create_message = {
                                    "raw": base64.urlsafe_b64encode(
                                        message.as_bytes()
                                    ).decode()
                                }
                                try:
                                    message = (
                                        assistant_service.users()
                                        .messages()
                                        .send(userId="me", body=create_message)
                                        .execute()
                                    )
                                except HttpError as error:
                                    print(f"An error occurred: {error}")
                                    message = None
                        except HttpError as error:
                            print(f"An error occurred: {error}")
                            message = None
            sleep(60)
