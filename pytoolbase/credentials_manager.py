from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from .my_logger import CustomLogger
import os
import logging


class CustomCredentialsManager:
    __custom_logger = None
    __token_path = None
    __path_class = None
    __scopes = [
        'https://www.googleapis.com/auth/gmail.compose'
        ,'https://www.googleapis.com/auth/chat.bot'
    ]
    __google_creds = None

    def __init__(self, path_manipulation_class):
        self.__custom_logger = CustomLogger('CustomCredentialsManager').custom_logger(logging.WARNING)
        self.__path_class = path_manipulation_class
        self.__token_path = self.__path_class.get_token_path()
        self.__cred_file_path = self.__path_class.get_credentials_path()

    def get_scopes(self):
        return self.__scopes

    def get_google_credentials(self):
        return self.__google_creds

    def generate_google_credentials(self):
        creds = self.__google_creds
        if os.path.exists(self.__token_path):
            creds = Credentials.from_authorized_user_file(self.__token_path, self.__scopes)
        if not creds or creds:
            if creds and creds and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__cred_file_path, self.__scopes)
                creds = flow.run_local_server(port=0)

        self.__google_creds = creds

        with open(self.__token_path, "w") as token:
            token.write(creds.to_json())

