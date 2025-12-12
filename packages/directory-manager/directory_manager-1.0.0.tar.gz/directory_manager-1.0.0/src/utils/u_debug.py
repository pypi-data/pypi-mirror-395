"""
***utils/u_debug.py***

A module for custom runtime tracing objects.

Features:
- DynamicLogger: inheriting from Logging.Logger object, designed as a basic logger
                 with required functionalities for directory module, including a program
                 exit in critical conditions.
"""

import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
from logging import Handler, getLoggerClass, Formatter, StreamHandler, LogRecord, DEBUG

__all__ = [
    'DynamicLogger',
    "default_logger"
]


class DynamicLogger(getLoggerClass()):
    """
    Custom logger class for easier handler processing.
    """
    def __init__(self, name : str, level : int = DEBUG):
        """
        Initiates an instance with no handlers, the object can initiate three different handlers and disable them at any time:
            -file streaming handler: streams logs to a file
            -console printing handler: prints logs to the terminal
            -error handler: exits the program at a specified logging level
        """
        super().__init__(name, level)
        self.setLevel(level)
        self.file_handler : Optional[Handler] = None
        self.stream_handler : Optional[Handler] = None
        self.exit_handler : Optional[Handler] = None
        self._exit_level : Optional[int] = None

    def init_file_handler(self, file_path : str, mode : str = 'w', max_size : int = 0, backup_count : int = 0, encoding : Optional[str] = None, delay : bool = False, 
                          errors : Optional[str] = None, log_format : Optional[str] = None, time_format : Optional[str] = None)->None:
        """
        Handles file streaming initialization and creates the file path if it does not exist, mode is set to 'a' for append if max_size is specified.
        """
        self.disable_file_handler()
        DynamicLogger._handle_path(file_path)
        self.file_handler = RotatingFileHandler(filename=file_path, mode=mode, maxBytes=max_size, backupCount=backup_count, encoding=encoding, delay=delay, errors=errors)
        formatter = Formatter(log_format, datefmt=time_format)
        self.file_handler.setFormatter(formatter)
        self.addHandler(self.file_handler)
        self.disable_error_handler(False)
        self.init_error_handler(self._exit_level)

    def init_stdout_handler(self, log_format : Optional[str] = None, time_format : Optional[str] = None)->None:
        """
        Handles the initialization of logging output onto the terminal.
        """
        self.disable_stream_handler()
        self.stream_handler = StreamHandler(sys.stdout)
        formatter = Formatter(log_format, datefmt=time_format)
        self.stream_handler.setFormatter(formatter)
        self.addHandler(self.stream_handler)
        self.disable_error_handler(False)
        self.init_error_handler(self._exit_level)

    def init_error_handler(self, level)->None:
        """
        Sets a level of logging that triggers a program exit, example: passing CRITICAL or 50 as an argument will stop the program from running once it hits a critical level log.
        """
        if level is None:
            return
        self.exit_handler = ExitHandler(level)
        self._exit_level = level
        self.addHandler(self.exit_handler)

    def disable_file_handler(self)->None:
        """
        Disables streaming logs to file.
        """
        if self.file_handler:
            self.removeHandler(self.file_handler)
            self.file_handler = None

    def disable_stream_handler(self)->None:
        """
        Disables printing logs to the console.
        """
        if self.stream_handler:
            self.removeHandler(self.stream_handler)
            self.stream_handler = None

    def disable_error_handler(self, reset_level: bool = True)->None:
        """
        Forgets the error flag if previously specified.
        """
        if self.exit_handler:
            self.removeHandler(self.exit_handler)
            self.exit_handler = None
        if reset_level:
            self._exit_level = None
    
    @staticmethod
    def _handle_path(path: str)->None:
        """
        Creates path to directory, reserved for class.
        """
        if not path:
            raise ValueError
        path_parts = Path(path).parts
        if len(path_parts) == 1:
            return
        dir_path, _ = path_parts[:-1], path_parts[-1]
        Path(*dir_path).mkdir(exist_ok=True)
        return None

class ExitHandler(Handler):
    def __init__(self, level : int = 0):
        super().__init__(level)

    def emit(self, record : LogRecord):
        if record.levelno >= self.level:
            sys.exit(1)

def default_logger(enable_file: bool = True, enable_sysout: bool = True, enable_error: bool = True)->DynamicLogger:
    file_format = "%(asctime)s - %(name)s - [%(levelname)s] - (%(lineno)s)%(funcName)s - %(message)s"
    stream_format = "%(name)s - [%(levelname)s] - %(message)s"
    time_format = None
    entry_level = 30
    logger : DynamicLogger = DynamicLogger(__name__, entry_level)
    if enable_file:
        file_path = "log/log.log"
        max_size = 1024 * 1024
        logger.init_file_handler(file_path=file_path, mode='w', max_size=max_size, log_format=file_format, time_format=time_format)
    if enable_sysout:
        logger.init_stdout_handler(stream_format, time_format)
    if enable_error:
        exit_level = 50
        logger.init_error_handler(level=exit_level)
    return logger

if __name__ == '__main__':
    print(__doc__)