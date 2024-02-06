import base64
import mimetypes
import os
from .configuration_file import Configuration
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .my_logger import CustomLogger
import logging
from .credentials_manager import CustomCredentialsManager


class SendEmailWithGoogleMail:
    __creds_class = None
    __creds = None
    __token_path = None
    __cred_file_path = None
    __gmail_env_file = None
    __path_class = None
    __config_class = None
    __email_body = None
    __attachment_file = None
    __custom_logger = None

    def __init__(self, email_body, attachment_file, path_manipulation_class):
        self.__custom_logger = CustomLogger('SendEmailWithGoogleMailClass').custom_logger(logging.WARNING)
        self.__path_class = path_manipulation_class
        self.__creds_class = CustomCredentialsManager(self.__path_class)
        self.__config_class = Configuration()
        self.__email_body = email_body
        self.__attachment_file = attachment_file
        self.__gmail_env_file = self.__config_class.get_value_from_env_file(
                                        os.path.join(self.__path_class.get_env_path(), '.gmail-env')
                                        )

    def send_email(self, with_attachments):
        self.__creds_class.generate_google_credentials()
        self.__creds = self.__creds_class.get_google_credentials()

        if with_attachments:
            self.__call_gmail_api_with_attachments(
                self.__email_body,
                self.__attachment_file
            )

    def __call_gmail_api_with_attachments(self, email_body, attachment_file):
        """
        For further info please refer to https://developers.google.com/gmail/api/guides/sending
        """
        try:
            service = build('gmail', 'v1', credentials=self.__creds)
            mime_message = EmailMessage()

            # Message body
            mime_message.set_content(email_body)

            mime_message["To"] = self.__gmail_env_file['message_to']
            mime_message["From"] = self.__gmail_env_file['message_from']
            mime_message["Subject"] = self.__gmail_env_file['message_subject']

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
