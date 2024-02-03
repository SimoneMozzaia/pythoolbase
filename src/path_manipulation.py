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

    def __init__(self):
        self.__custom_logger = logging.getLogger(__name__)
        self.__src_path = Path(os.getcwd()).resolve().parents[1]

    def get_secrets_path(self, local_secrets_folder):
        return os.path.join(self.__src_path, local_secrets_folder)

    def get_external_files_path(self, local_ext_files_folder):
        return os.path.join(self.__src_path, local_ext_files_folder)
