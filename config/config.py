import os


class Config:

    def __init__(self):
        self.credentials = os.environ.get("CREDENTIALS")
        self.assistant_scopes = os.environ.get("ASSISTANT_SCOPES")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.emails_to_listen_for = os.environ.get("EMAIL_TO_LISTEN_FOR")
        self.main_scopes = os.environ.get("MAIN_SCOPES")


config = Config()
