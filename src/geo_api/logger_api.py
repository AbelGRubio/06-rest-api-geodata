"""
    Aqui se define como va a ser el logger
"""
import logging
import os.path
from logging import LogRecord
from logging.handlers import TimedRotatingFileHandler

from colorama import Fore, Style


class ColoredFormatter (logging.Formatter):
    """
    Custom formatter
    """
    def format(self, record: LogRecord) -> str:
        """custom format"""
        level_colors = {
            logging.DEBUG: Fore.BLUE,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore. YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT}

        level_color = level_colors.get(record.levelno, "")
        formatted_message = super().format(record)
        return f" {level_color}{formatted_message}{Style.RESET_ALL}"


class LoggerApi(logging.Logger):
    """Custom logger """

    def __init__(self, name: str = None, level: int = logging.DEBUG):
        if not name:
            name = 'api'
        super().__init__(name, level)
        self._folder_name = '.logs'
        self.file_name = f'{self._folder_name}/{self.name}.log'
        self.msg_format = '%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
        self.datetime_format = "%Y-%m-%d %H:%M:%S"
        self._configure_logger()
        self._create_file_handler()

    def _configure_logger(self) -> None:
        """configura el logger"""
        self.custom_console_handler = logging.StreamHandler()
        self.custom_console_handler.setLevel(logging.DEBUG)

        formatter = ColoredFormatter(self.msg_format, self.datetime_format)
        self.custom_console_handler.setFormatter(formatter)

        self.addHandler(self.custom_console_handler)

    def _create_file_handler(self) -> None:
        """Create file handler que cambia dia a dia"""
        if not os.path.exists(self._folder_name):
            os.mkdir(self._folder_name)

        self.custom_file_handler = TimedRotatingFileHandler(
            self.file_name,
            when='midnight', interval=1, backupCount=4)
        self.custom_file_handler.setLevel (logging.DEBUG)

        file_formatter = logging.Formatter(
            self.msg_format, self.datetime_format)
        self.custom_file_handler.setFormatter(file_formatter)

        self.addHandler(self.custom_file_handler)
