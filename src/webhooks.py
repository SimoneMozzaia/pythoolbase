from json import dumps
from httplib2 import Http
import logging


class GoogleWebhook:
    __instance = None
    __custom_logger = None
    __webhook_section = None
    __app_message = None

    def __init__(self):
        self.__custom_logger = logging.getLogger('__main__.' + __name__)
    
    def create_app_message_for_webhook(self, *args):
        self.__app_message = {"text": f"{args[0]}"}
        
        return self.__app_message
    
    def trigger_google_webhook(self, hook_url, *args):
        self.__custom_logger.info(f"Sending info to google space")
        
        app_message = self.__app_message        
        message_headers = {"Content-Type": "application/json; charset=UTF-8"}
        http_obj = Http()
        response = http_obj.request(
            uri=hook_url,
            method="POST",
            headers=message_headers,
            body=dumps(app_message),
        )
        
        self.__custom_logger.debug(f"response: {response}")
