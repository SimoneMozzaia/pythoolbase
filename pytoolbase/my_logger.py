import logging
import os
from datetime import date


class CustomLogger(logging.Logger):
    __class_name = None

    def __init__(self, class_name):
        if not os.path.exists('logs\\'):
            os.mkdir('logs\\')
        self.__class_name = class_name
        super().__init__(class_name)

    def custom_logger(self, logging_level):
        logger = logging.getLogger(self.__class_name)
        logger.setLevel(logging_level)
        # Create file handler
        file_handler = logging.FileHandler(
            filename=os.path.join('.\logs', str(date.today()) + '-' + self.__class_name),
            mode='w'
        )
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add handler and formatters to the logger
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger
