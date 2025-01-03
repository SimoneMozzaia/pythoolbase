import json
import os.path
import sys
from dotenv import dotenv_values, set_key, load_dotenv
from .my_logger import CustomLogger
import logging


class Configuration:
    """
    A simple Configuration class. Used to manage configuration methods.
    It's also used to get the path to relevant folders
    such as secrets or external_files. These folders are used by various utilities

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
        env_path    Path where the .env files are stored (f.e. r'.\secrets\env')
        secrets_path    Path where the secrets files are stored (f.e. r'.\secrets)
        query_path  Path where the .sql queries are stored (f.e. r'.\secrets\queries')
    """
    __custom_logger = None
    __env_file_path = None
    __custom_handler = None
    __env_path = None
    __secrets_path = None
    __query_path = None
    __env_file_loaded = False
    __general_env_filename = '.env'
    __is_env_file_loaded = False
    __loaded_env_file = None
        
    def __init__(self, env_path, secrets_path, query_path, log_level):
        self.__custom_logger = CustomLogger('ConfigurationClass').custom_logger(log_level)
        self.__env_path = env_path
        self.__secrets_path = secrets_path
        self.__query_path = query_path
        self.load_env_file()
        self.__custom_logger.info(
            f'Initializing Configuration Class. Parameters: {env_path}, {secrets_path}, {query_path}, {log_level}'
        )

    def __get_general_env_file_path(self):
        """Getter for the path to the generic .env file
        Return:
            The path to the file
        """
        self.__custom_logger.info(f'__get_general_env_file_path')
        path = os.path.join(self.__env_path, self.__general_env_filename)
        self.__custom_logger.debug(f'{path}')

        return path

    def load_env_file(self, country=None, environment=None, direct_path=None):
        """
        Loads a .env file to manage application secrets.
        If country and environments are specified then the function loads a specific country/env file
        If a direct path is specified, then it tries to load the file referenced by that path

        Args:
            country: country related to the file that I want to load
            environment: prod/qa/dev...
            direct_path: a path pointing to a specific .env file

        Returns:
            A specific country/env environment file OR
            A generic configuration environment file OR
            A specific configuration environment file

        """
        self.__custom_logger.info(f'load_env_file')

        if direct_path is not None:
            self.__custom_logger.info(f'loading {direct_path} env file')
            return dotenv_values(direct_path)

        if country is not None and environment is not None:
            if os.path.exists(self.__get_country_env_file(country, environment)):
                self.__custom_logger.info(f'loading {country}, {environment} env file')
                return dotenv_values(self.__get_country_env_file(country, environment))

        if not self.__is_env_file_loaded:
            if os.path.exists(self.__env_path):
                self.__custom_logger.info(f'loading dotenv file')
                self.__env_file_path = self.__env_path
                self.__loaded_env_file = dotenv_values(self.__get_general_env_file_path())

                if self.__loaded_env_file is not None:
                    self.__custom_logger.info(f'file loaded')
                    self.__is_env_file_loaded = True

                    return self.__loaded_env_file

                else:
                    self.__custom_logger.critical(f'Cannot load the file')
                    sys.exit(98)

        else:
            self.__custom_logger.info(f'Returning already loaded generic .env file')
            return self.__loaded_env_file

    def set_env_file_key(self, key_to_set, key_value):
        self.__custom_logger.info(f'set_env_file_key. Parameters: {key_to_set}, {key_value}')

        load_dotenv(self.__env_file_path)
        os.environ[key_to_set] = key_value

        # Write changes to .env file.
        set_key(self.__env_file_path, key_to_set, os.environ[key_to_set])
        
    def get_value_from_json(self, json_file, key, sub_key):
        """Return the value of the specified key; sub_key pair from a json file.

        Args:
            self (Configuration): Instance of the Configuration Class
            json_file (str): The path to the json file to open
            key (str): The key to search for
            sub_key (str): The subkey of the key

        Returns:
            str: The value of the specified key;sub_key pair (if exists)

        Raises:
            KeyError    If the key:sub_key pair is not found
            Exception   If the json file can't be opened or can't be found
            JSONDecodeError     If the file is not a JSON or can't be decoded as such
        """
        self.__custom_logger.info(f'get_value_from_json. Parameters: {json_file}, {key}, {sub_key}')
        try:
            with open(json_file) as jf:
                data = json.load(jf)
                return data[key][sub_key]

        except KeyError:
            self.__custom_logger.critical(f'[{key}][{sub_key}] pair not found in file {json_file}.')
            raise KeyError('Bad key;sub_key pair') from None

        except json.decoder.JSONDecodeError:
            self.__custom_logger.critical(f'File {json_file} is not a JSON or has a bad format.')
            raise json.decoder.JSONDecodeError("Expecting value", json_file, 1) from None

        except Exception('Critical failure while loading json'):
            self.__custom_logger.critical(f'Cannot load json file {json_file}. File does not exists.')
            sys.exit(97)

    def get_log_level_from_log_key(self, log_key):
        string = self.__loaded_env_file[log_key]
        return logging.getLevelNamesMapping()[string]

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

    def __get_country_env_file(self, country, environment):
        self.__custom_logger.info(f'get_country_env_file')

        country_env_filename = '.' + country + '-' + environment + '-env'
        return os.path.join(self.__env_path, country_env_filename)
