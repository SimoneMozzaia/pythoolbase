import logging
import os
from datetime import date

'''Logger module hints

In the main module call getLogger(__name__)
Replace getLogger(__name__) in the auxiliary module by getLogger('__main__.' + __name__). 
'''
if not os.path.exists('logs\\'):
    os.mkdir('logs\\')

custom_logger = logging.getLogger(__name__)
custom_logger.setLevel(logging.DEBUG)

custom_handler = logging.FileHandler(r"logs\\" + str(date.today()) + '_' + __name__, mode='w')
custom_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

custom_handler.setFormatter(custom_formatter)

custom_logger.addHandler(custom_handler)