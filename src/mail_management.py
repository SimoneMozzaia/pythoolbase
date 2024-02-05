import base64
import mimetypes
import os
from path_manipulation import PathManipulation
from configuration_file import Configuration
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SendEmailWithGoogleMail:
    __creds = None
    __token_path = r'.\secrets\token.json'
    __cred_file_path = r'.\secrets\credentials.json'
    __ext_file_path = r'.\external_files'
    __scopes = ['https://www.googleapis.com/auth/gmail.compose']
    __gmail_env_file = None
    __path_class = None
    __config_class = None

    def __init__(self):
        self.__path_class = PathManipulation()
        self.__config_class = Configuration()
        self.__gmail_env_file = self.__config_class.get_value_from_env_file(
                                        os.path.join(self.__path_class.get_env_path(), '.gmail-env')
                                        )

    def send_email(self, with_attachments):
        self.__generate_credentials(creds=self.__creds,
                                    token_path=self.__token_path,
                                    cred_file_path=self.__cred_file_path
                                    )
        if with_attachments:
            self.__call_gmail_api_with_attachments(os.path.join(self.__ext_file_path, 'test.xlsx'))

    def __generate_credentials(self, creds, token_path, cred_file_path):
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(self.__token_path, self.__scopes)
        if not creds or creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_file_path, self.__scopes)
                creds = flow.run_local_server(port=0)

        self.__creds = creds

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    def __call_gmail_api_with_attachments(self, attachment_file):
        """
        For further info please refer to https://developers.google.com/gmail/api/guides/sending
        """
        try:
            service = build('gmail', 'v1', credentials=self.__creds)
            mime_message = EmailMessage()

            # Message body
            mime_message.set_content("Hi, this is automated mail with attachment.\nPlease do not reply.")

            mime_message["To"] = self.__gmail_env_file['message_to']
            mime_message["From"] = self.__gmail_env_file['message_from']
            mime_message["Subject"] = "Automated message"

            # Manage attachments
            attachment_filename = attachment_file

            # guessing the MIME type
            type_subtype, _ = mimetypes.guess_type(attachment_filename)
            maintype, subtype = type_subtype.split("/")

            with open(attachment_filename, "rb") as fp:
                attachment_data = fp.read()
            mime_message.add_attachment(attachment_data, maintype, subtype)

            # Encode the message
            encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

            # Create and send
            create_message = {"raw": encoded_message}
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')

        except HttpError as error:
            print(f'Error: {error}')


g = SendEmailWithGoogleMail()
g.send_email(True)
