import logging
import json
import os.path
from dotenv import dotenv_values


class Configuration:
    """A simple Configuration class. Used to manage configuration methods.

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
    """
    __custom_logger = None
        
    def __init__(self):
        self.__custom_logger = logging.getLogger(__name__)

    def get_value_from_env_file(self, filepath):
        """

        """
        self.__custom_logger.info(f'get_value_from_env_file')

        if os.path.exists(filepath):
            return dotenv_values(filepath)

        self.__custom_logger.critical(f'Cannot load {filepath} file')
        return None
        
    def get_value_from_json(self, json_file, key, sub_key):
        """
        Return the value of the specified key; sub_key pair from a json file.

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
