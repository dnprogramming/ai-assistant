import os


class Config:

    def __init__(self):
        self.gmail_account_data = os.environ.get("GMAIL_ACCOUNT_DATA")
        self.bard_api_key = os.environ.get("BARD_API_KEY")
        self.email_to_listen_for = os.environ.get("EMAIL_TO_LISTEN_FOR")


config = Config()

# Use the retrieved values as needed
