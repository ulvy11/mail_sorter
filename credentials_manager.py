import os

from typing import NoReturn

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class CredentialsManager:
    __SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]
    __PATH = "token.json"

    def __new__(self) -> NoReturn:
        raise TypeError("This class cannot be instantiated directly.")

    @classmethod
    def set_path(cls, path: str):
        cls.__PATH = path

    @classmethod
    def set_scope(cls, scope: list[str]):
        cls.__SCOPES = scope

    @classmethod
    def get_creds(cls) -> Credentials:
        creds: Credentials = None
        if os.path.exists(cls.__PATH):
            creds = Credentials.from_authorized_user_file("token.json", cls.__SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", cls.__SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(cls.__PATH, "w") as token:
                token.write(creds.to_json())
        return creds
