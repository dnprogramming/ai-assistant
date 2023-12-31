from config import config
from time import sleep
from utils import gmail as service

class Main:
    def __init__(self):
        self.target_email = config.Config().email_to_listen_for

    def main(self):
        while True:
            results = service.connect_to_gmail().users().messages().list(userId='me', q=f'from:{self.target_email}').execute()
            messages = results.get('messages', [])

            if messages:
                for message in messages:
                    message = service.connect_to_gmail().users().messages().get(userId='me', id=message['id']).execute()
                    if 'UNREAD' in message['labelIds']:
                        service.connect_to_gmail().users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            sleep(60)