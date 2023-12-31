import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import config

ASSISTANT_SERVICE_ACCOUNT_INFO = config.Config().assistant_credentials
MAIN_SERVICE_ACCOUNT_INFO = config.Config().main_credentials

ASSISTANT_SCOPES = [config.Config().assistant_scopes]
MAIN_SCOPES = [config.Config().main_scopes]


class Gmail:

    def connect_to_assistant_google():
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

        return service

    def connect_to_calendar():
        flow = InstalledAppFlow.from_client_secrets_file(
            MAIN_SERVICE_ACCOUNT_INFO, scopes=MAIN_SCOPES
        )

        flow.run_local_server()
        credentials = flow.credentials

        service = build("calendar", "v3", credentials=credentials)

        return service

    def connect_to_main_google():
        flow = InstalledAppFlow.from_client_secrets_file(
            MAIN_SERVICE_ACCOUNT_INFO, scopes=MAIN_SCOPES
        )

        flow.run_local_server()
        credentials = flow.credentials

        service = build("gmail", "v1", credentials=credentials)

        return service
