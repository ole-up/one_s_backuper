import logging
import logging.handlers as handlers
import sys
import os

sys.path.append('../')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'utils.log')

formatter = logging.Formatter(
    '%(asctime)s %(levelname)-10s %(module)-10s %(message)s')

utils_log_handler = handlers.TimedRotatingFileHandler(PATH, when='midnight', interval=1, backupCount=14,
                                                      encoding='utf-8')
utils_log_handler.setFormatter(formatter)
utils_log_handler.setLevel(logging.CRITICAL)

utils_logger = logging.getLogger('utils')
utils_logger.addHandler(utils_log_handler)
utils_logger.setLevel(logging.DEBUG)
