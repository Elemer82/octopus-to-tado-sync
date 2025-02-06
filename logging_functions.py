import inspect
import logging
import logging.handlers
import os

def create_debug_info_console_logging(file_str: str,) -> logging:
    """
    Creates a logging type of object and returns it
    :param file_str: uses thi string to specify what the output file should be named
    :return: An object of type logging
    """
    log = None
    try:
        print(inspect.stack()[0][3]) # function_name
        log = logging.getLogger(__name__)
        log.debug("Log object created")
        log.setLevel("DEBUG")

        formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
        debug_formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{",
                                            datefmt="%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel("DEBUG")
        log.addHandler(console_handler)
        log.debug("Console handler added to log object")

        info_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-info.log", when="midnight",
                                                                      backupCount=7)
        info_file_handler.setFormatter(formatter)
        info_file_handler.setLevel("INFO")
        log.addHandler(info_file_handler)
        log.info("Info file handler added to log object")


        debug_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-debug.log", when="midnight",
                                                                      backupCount=7)
        debug_file_handler.setFormatter(debug_formatter)
        debug_file_handler.setLevel("DEBUG")
        log.addHandler(info_file_handler)
        log.info("Debug file handler added to log object")
    except Exception as ex:
        file_name = os.path.split(inspect.stack()[0][1])[1]
        function_name = inspect.stack()[0][3]
        message = f"{file_name} : {function_name} : An exception of type {type(ex)} occurred. Arguments:\n{ex.args}"
        print(message)
    finally:
        return log


