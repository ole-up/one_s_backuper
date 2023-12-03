import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import os

sys.path.append('../')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'backuper.log')

formatter = logging.Formatter(
    '%(asctime)s - %(message)s')

backuper_log_handler = TimedRotatingFileHandler(PATH, when='midnight', interval=1, backupCount=14, encoding='utf-8')
backuper_log_handler.setFormatter(formatter)
backuper_log_handler.setLevel(logging.INFO)

backuper_logger = logging.getLogger('backuper')
backuper_logger.addHandler(backuper_log_handler)
backuper_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    backuper_logger.info('Тест логгера')
