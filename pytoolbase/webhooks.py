from json import dumps
from httplib2 import Http
import logging
from .my_logger import CustomLogger


class GoogleWebhook:
    __custom_logger = None
    __app_message = None
    __hook_url = None

    def __init__(self, hook_url, log_level):
        self.__custom_logger = CustomLogger('GoogleWebhook').custom_logger(log_level)
        self.__custom_logger.info(f'Initializing GoogleWebhook Class')
        self.__hook_url = hook_url

    def send_message_to_google_space(self, *args):
        self.__custom_logger.info('send_message_to_google_space')
        self.__create_app_message_for_webhook(*args)
        self.__trigger_google_webhook()
    
    def __create_app_message_for_webhook(self, *args):
        self.__custom_logger.info('__create_app_message_for_webhook')
        self.__app_message = {"text": f"{args[0]}"}
    
    def __trigger_google_webhook(self):
        self.__custom_logger.info(f"__trigger_google_webhook")
        
        app_message = self.__app_message        
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=self.__hook_url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        
        self.__custom_logger.debug(f"response: {response}")


class MicrosoftTeamsWebhook:
    __custom_logger = None
    __app_message = None
    __hook_url = None

    def __init__(self, hook_url, log_level):
        self.__custom_logger = CustomLogger('MicrosoftTeamsWebhook').custom_logger(log_level)
        self.__custom_logger.info(f'Initializing MicrosoftTeamsWebhook Class')
        self.__hook_url = hook_url

    def send_message_to_teams_chat(self, *args):
        self.__custom_logger.info('send_message_to_teams_chat')
        self.__create_app_message_for_webhook(*args)
        self.__trigger_teams_webhook()

    def __create_app_message_for_webhook(self, *args):
        self.__custom_logger.info('__create_app_message_for_webhook')
        self.__app_message = {"output": f"{args[0]}"}

    def __trigger_teams_webhook(self):
        self.__custom_logger.info(f"__trigger_teams_webhook")

        app_message = self.__app_message
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=self.__hook_url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )

        self.__custom_logger.debug(f"response: {response}")