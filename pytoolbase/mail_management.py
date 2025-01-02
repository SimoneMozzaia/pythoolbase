import base64
import mimetypes
import os
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .my_logger import CustomLogger
from .credentials_manager import CustomCredentialsManager


class SendEmailWithGoogleMail:
    __creds_class = None
    __creds = None
    __token_path = None
    __cred_file_path = None
    __gmail_env_file = None
    __config_class = None
    __email_subject = None
    __email_body = None
    __attachment_file = None
    __attachment_filename = None
    __custom_logger = None

    def __init__(self, email_subject, email_body, attachment_file, attachment_filename, config_class):
        self.__config_class = config_class
        self.__custom_logger = CustomLogger('SendEmailWithGoogleMailClass').custom_logger(
            self.__config_class.get_log_level_from_log_key("send_mail_with_google_mail_log_level")
        )
        self.__creds_class = CustomCredentialsManager(
            self.__config_class,
            self.__config_class.get_log_level_from_log_key("custom_credential_manager_log_level")
        )
        self.__email_subject = email_subject
        self.__email_body = email_body
        self.__attachment_file = attachment_file
        self.__attachment_filename = attachment_filename
        self.__gmail_env_file = self.__config_class.get_value_from_env_file(
                                        os.path.join(self.__config_class.get_env_path(), '.gmail-env')
                                        )
        self.__custom_logger.info(
            f'Initializing SendEmailWithGoogleMail Class. Parameters: {email_subject}, {email_body}, {attachment_file}, {attachment_filename}'
        )

    def send_email(self, with_attachments, maintype=None, subtype=None):
        """Method to send an email with the Google Mail API service.
        If no type, subtype are provided then the next methods will
        guess the MIME type themselves.

        Args:
            with_attachments:
            maintype:
            subtype:

        Returns:

        """
        self.__custom_logger.info(f'send_email. Parameters: {with_attachments}, {maintype}, {subtype}')
        self.__creds_class.generate_google_user_credentials()
        self.__creds = self.__creds_class.get_google_user_credentials()

        if with_attachments:
            self.__call_gmail_api_with_attachments(maintype, subtype)

    def __call_gmail_api_with_attachments(self, maintype, subtype):
        """
        For further info please refer to https://developers.google.com/gmail/api/guides/sending
        """
        self.__custom_logger.info(f'__call_gmail_api_with_attachments. Parameters: {maintype}, {subtype}')
        try:
            service = build('gmail', 'v1', credentials=self.__creds)
            mime_message = EmailMessage()

            # Message body
            mime_message.set_content(self.__email_body)

            mime_message["To"] = self.__gmail_env_file['message_to']
            mime_message["From"] = self.__gmail_env_file['message_from']
            mime_message["Subject"] = self.__email_subject

            # Manage attachments
            attachment_file = self.__attachment_file
            attachment_filename = self.__attachment_filename

            # guessing the MIME type if no type, subtype are provided
            if maintype is None or subtype is None:
                type_subtype, _ = mimetypes.guess_type(attachment_file)
                maintype, subtype = type_subtype.split("/")
            else:
                maintype = maintype
                subtype = subtype

            with open(attachment_file, "rb") as fp:
                attachment_data = fp.read()

            mime_message.add_attachment(attachment_data, maintype, subtype, filename=attachment_filename)

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
