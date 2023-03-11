import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


def get_logger() -> logging.Logger:
    """
    Initiated the logger

    :return: get the logger to register what it is doing the programme
    """
    nameLogger = "logger_api"
    logger = logging.getLogger(nameLogger)
    logger.setLevel(logging.INFO)
    folder = 'log'
    if not os.path.exists(folder):
        os.mkdir(folder)
    fh = TimedRotatingFileHandler(
        os.path.join(folder,
                     '.'.join([nameLogger, folder])),
        when='midnight')
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s, %(funcName)s] %(levelname)s '
                                  '%(message)s',
                                  datefmt='%d/%b/%Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.info("####################  logger initiated  ####################")
    return logger


LOGGER = get_logger()
