import os
from pathlib import Path
import logging


class PathManipulation:
    """A simple path manipulation class. It's used to get the path to relevant folders
    such as secrets or external_files. These folders are used by various utilities.

    Attributes:
        custom_logger   Instance of the custom logger class. Used for logging purposes
        src_path    Path to the project root
    """
    __custom_logger = None
    __src_path = None
    __env_path = r'.\secrets\env'
    __general_env_filename = '.env'

    def __init__(self):
        self.__custom_logger = logging.getLogger(__name__)
        self.__src_path = Path(os.getcwd()).resolve().parents[1]

    def get_secrets_path(self, local_secrets_folder):
        return os.path.join(self.__src_path, local_secrets_folder)

    def get_external_files_path(self, local_ext_files_folder):
        return os.path.join(self.__src_path, local_ext_files_folder)

    def get_general_env_file(self):
        """Getter for the generic .env file
        Return:
            The .env file containing general configurations
        """
        return os.path.join(self.__env_path, self.__general_env_filename)

    def get_env_path(self):
        """Getter for the path to the .env folder
            Return:
                The path to the .env folder
        """
        return self.__env_path

    def get_country_env_file(self, country, environment):
        country_env_filename = '.' + country + '-' + environment + '-env'
        return os.path.join(self.__env_path, country_env_filename)
