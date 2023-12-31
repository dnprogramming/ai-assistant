from google.oauth2 import service_account
from config.config import config
import googleapiclient.discovery

SERVICE_ACCOUNT_INFO = config().gmail_account_data

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def connect_to_gmail():
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )

    service = googleapiclient.discovery.build("gmail", "v1", credentials=credentials)

    return service


def connect_to_calendar():
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )

    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

    return service


if __name__ == "__main__":
    service = connect_to_gmail()
    calendar = connect_to_calendar()
