import logging
import sys
import os

sys.path.append('../')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'backuper.log')

formatter = logging.Formatter(
    '%(asctime)s %(levelname)-10s %(module)-10s %(message)s')

backuper_log_handler = logging.FileHandler(PATH, encoding='utf-8')
backuper_log_handler.setFormatter(formatter)
backuper_log_handler.setLevel(logging.INFO)

backuper_logger = logging.getLogger('backuper')
backuper_logger.addHandler(backuper_log_handler)
backuper_logger.setLevel(logging.INFO)
