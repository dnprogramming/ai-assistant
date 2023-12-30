from google.oauth2 import service_account
import googleapiclient.discovery

SERVICE_ACCOUNT_FILE = '/service_account_key.json'

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def connect_to_gmail():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

    return service

if __name__ == "__main__":
    # Connect to Gmail
    service = connect_to_gmail()
