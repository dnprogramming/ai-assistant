import os


class Config:

    def __init__(self):
        self.assistant_credentials = os.environ.get("ASSISTANT_CREDENTIALS")
        self.assistant_scopes = os.environ.get("ASSISTANT_SCOPES")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.email_to_listen_for = os.environ.get("EMAIL_TO_LISTEN_FOR")
        self.main_credentials = os.environ.get("MAIN_CREDENTIALS")
        self.main_scopes = os.environ.get("MAIN_SCOPES")


config = Config()

# Use the retrieved values as needed
