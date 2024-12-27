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
    __user_scopes = [
        'https://www.googleapis.com/auth/gmail.compose'
    ]
    __service_account_scopes = [
        'https://www.googleapis.com/auth/chat.bot'
    ]
    __google_user_creds = None
    __user_cred_file_path = None
    __service_acc_cred_file_path = None

    def __init__(self, path_manipulation_class, log_level):
        self.__custom_logger = CustomLogger('CustomCredentialsManager').custom_logger(log_level)
        self.__path_class = path_manipulation_class
        self.__token_path = self.__path_class.get_token_path()
        self.__user_cred_file_path = self.__path_class.get_user_credentials_path()
        self.__service_acc_cred_file_path = self.__path_class.get_service_account_credentials_path()
        self.__custom_logger.info(f'Initializing CustomCredentialsManager Class. Parameter: {path_manipulation_class}')

    def get_user_scopes(self):
        self.__custom_logger.info(f'get_user_scopes')
        return self.__user_scopes

    def get_service_account_scopes(self):
        self.__custom_logger.info(f'get_service_account_scopes')
        return self.__service_account_scopes

    def get_google_user_credentials(self):
        self.__custom_logger.info(f'get_google_user_credentials')
        return self.__google_user_creds

    def generate_google_user_credentials(self):
        self.__custom_logger.info(f'generate_google_user_credentials')

        creds = self.__google_user_creds
        if os.path.exists(self.__token_path):
            creds = Credentials.from_authorized_user_file(self.__token_path, self.__user_scopes)

        if not creds or creds:
            if creds and creds and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__user_cred_file_path, self.__user_scopes)
                creds = flow.run_local_server(port=0)

        self.__google_user_creds = creds

        with open(self.__token_path, "w+") as token:
            token.write(creds.to_json())

