import config as config
import gmail as service

class Main:
    def __init__(self):
        self.target_email = config.Config().email_to_listen_for

    def main(self):
        while True:
            results = service.users().messages().list(userId='me', q=f'from:{self.target_email}').execute()
            messages = results.get('messages', [])

            if messages:
                for message in messages:
                    message = service.users().messages().get(userId='me', id=message['id']).execute()
                    print(message['snippet'])
            time.sleep(60)