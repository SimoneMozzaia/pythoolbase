import os
import logging
from .my_logger import CustomLogger


class PathManipulation:
    """A simple path manipulation class. It's used to get the path to relevant folders
    such as secrets or external_files. These folders are used by various utilities.

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
        env_path    Path where the .env files are stored (f.e. r'.\secrets\env')
        secrets_path    Path where the secrets files are stored (f.e. r'.\secrets)
        query_path  Path where the .sql queries are stored (f.e. r'.\secrets\queries')
    """
    __custom_logger = None
    __custom_handler = None
    __env_path = None
    __secrets_path = None
    __query_path = None
    __general_env_filename = '.env'

    def __init__(self, env_path, secrets_path, query_path):
        self.__custom_logger = CustomLogger('PathManipulationClass').custom_logger(logging.WARNING)
        self.__env_path = env_path
        self.__secrets_path = secrets_path
        self.__query_path = query_path
        self.__custom_logger.info(f'Initializing PathManipulation Class. Parameters: {env_path}, {secrets_path}'
                                  f', {query_path}')

    def get_general_env_file(self):
        """Getter for the generic .env file
        Return:
            The .env file containing general configurations
        """
        self.__custom_logger.info(f'get_general_env_file')
        return os.path.join(self.__env_path, self.__general_env_filename)

    def get_env_path(self):
        """Getter for the path to the .env folder
            Return:
                The path to the .env folder
        """
        self.__custom_logger.info(f'get_env_path')
        return self.__env_path

    def get_secrets_path(self):
        self.__custom_logger.info(f'get_secrets_path')
        return self.__secrets_path

    def get_token_path(self):
        self.__custom_logger.info(f'get_token_path')
        return os.path.join(self.__secrets_path, 'token.json')

    def get_user_credentials_path(self):
        self.__custom_logger.info(f'get_user_credentials_path')
        return os.path.join(self.__secrets_path, 'oauth2_client_user_not_service.json')

    def get_service_account_credentials_path(self):
        self.__custom_logger.info(f'get_service_account_credentials_path')
        return os.path.join(self.__secrets_path, 'service_account.json')

    def get_queries_path(self):
        self.__custom_logger.info(f'get_queries_path')
        return self.__query_path

    def get_country_env_file(self, country, environment):
        self.__custom_logger.info(f'get_country_env_file')

        country_env_filename = '.' + country + '-' + environment + '-env'
        return os.path.join(self.__env_path, country_env_filename)
