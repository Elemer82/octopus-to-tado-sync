"""
This module provides functions to create a logging object that can log to both console and a Tkinter Text widget.
2025-06-03 - Created by Elemer Gazda
"""

# Built-in modules
import inspect
import logging
import logging.handlers
import os
import threading
from time import sleep
# Third-party modules
import tkinter


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.text.configure(state='normal')

    def emit(self, record):
        """This method is called when a log message is emitted"""
        msg = self.format(record)
        """def append():
            self.text.configure(state='normal')
            self.text.insert(tkinter.END, msg + '\n')
            # self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tkinter.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
        """
        
        self.text.insert(tkinter.END, msg + '\n')
        # Autoscroll to the bottom
        self.text.yview(tkinter.END)


def create_debug_info_console_logger(file_str: str) -> logging.Logger:
    """
    Creates a logging type of object and returns it
    :param file_str: uses thi string to specify what the output file should be named
    :return: An object of type logging
    """
    logger_ = logging.getLogger(__name__)
    try:
        print(inspect.stack()[0][3]) # function_name
        logger_ = logging.getLogger(__name__)
        logger_.debug("Log object created")
        logger_.setLevel("DEBUG")

        formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
        debug_formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{",
                                            datefmt="%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel("DEBUG")
        logger_.addHandler(console_handler)
        logger_.debug("Console handler added to log object")

        info_timed_rotating_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-info.log", when="midnight", backupCount=7)
        info_timed_rotating_file_handler.setFormatter(formatter)
        info_timed_rotating_file_handler.setLevel("INFO")
        logger_.addHandler(info_timed_rotating_file_handler)
        logger_.info("Info file handler added to log object")


        debug_timed_rotated_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-debug.log", when="midnight", backupCount=7)
        debug_timed_rotated_file_handler.setFormatter(debug_formatter)
        debug_timed_rotated_file_handler.setLevel("DEBUG")
        logger_.addHandler(debug_timed_rotated_file_handler)
        logger_.info("Debug file handler added to log object")
    except Exception as ex:
        file_name = os.path.split(inspect.stack()[0][1])[1]
        function_name = inspect.stack()[0][3]
        message = f"{file_name} : {function_name} : An exception of type {type(ex)} occurred. Arguments:\n{ex.args}"
        print(message)
    finally:
        return logger_
    

def create_console_file_tkinter_logger(file_str: str, tkinter_text) -> logging.Logger:
    """
    Creates a logging type of object and returns it
    :param file_str: uses thi string to specify what the output file should be named
    :return: An object of type logging
    """
    logger_ = logging.getLogger(__name__)
    try:
        print(inspect.stack()[0][3]) # function_name
        logger_ = logging.getLogger(__name__)
        logger_.debug("Log object created")
        logger_.setLevel("DEBUG")

        # Set the logger to use the same thread as the main thread
        logger_.handlers = []  # Clear any existing handlers
        logger_.propagate = False
        logger_.debug("Log object handlers cleared")
        logger_.debug("Log object propagate set to False")
        logger_.debug("Log object set to main thread")
        
        # Create formatters
        # Set the format for the log messages
        formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
        debug_formatter = logging.Formatter("{asctime} - {levelname} - {funcName} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")
        clean_formatter = logging.Formatter("{message}", style="{")
        
        # Create Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG) # Set the level to DEBUG or INFO as needed 
        # Set the console handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        console_handler._lock = threading.Lock()
        console_handler._thread = threading.main_thread()
        console_handler._thread_id = threading.get_ident()
        console_handler._thread_name = threading.current_thread().name
        # Add the console handler to the logger
        logger_.addHandler(console_handler)
        logger_.debug("Console handler added to log object")

        # Create TimedRotatingFileHandler info_file handler
        info_timed_rotating_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-info.log", when="midnight", backupCount=7)
        info_timed_rotating_file_handler.setFormatter(formatter)
        info_timed_rotating_file_handler.setLevel(logging.INFO)
        # Set the file handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        info_timed_rotating_file_handler._lock = threading.Lock()
        info_timed_rotating_file_handler._thread = threading.main_thread()
        info_timed_rotating_file_handler._thread_id = threading.get_ident()
        info_timed_rotating_file_handler._thread_name = threading.current_thread().name
        logger_.addHandler(info_timed_rotating_file_handler)
        logger_.info("Info file handler added to log object")

        # Create TimedRotatingFileHandler debug_file handler
        debug_timed_rotating_file_handler = logging.handlers.TimedRotatingFileHandler(filename=f"{file_str}-debug.log", when="midnight", backupCount=7)
        debug_timed_rotating_file_handler.setFormatter(debug_formatter)
        debug_timed_rotating_file_handler.setLevel(logging.DEBUG)
        # Set the file handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        debug_timed_rotating_file_handler._lock = threading.Lock()
        debug_timed_rotating_file_handler._thread = threading.main_thread()
        debug_timed_rotating_file_handler._thread_id = threading.get_ident()
        debug_timed_rotating_file_handler._thread_name = threading.current_thread().name
        # Add the file handler to the logger
        logger_.addHandler(debug_timed_rotating_file_handler)
        logger_.debug("Debug file handler set to main thread")
        
        # Create FileHandler debug file handler
        debug_file_handler = logging.FileHandler(filename=f"{file_str}-FH-Debug.log", mode='a')
        debug_file_handler.setFormatter(debug_formatter)
        debug_file_handler.setLevel(logging.DEBUG)
        # Set the file handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        debug_file_handler._lock = threading.Lock()
        debug_file_handler._thread = threading.main_thread()
        debug_file_handler._thread_id = threading.get_ident()
        debug_file_handler._thread_name = threading.current_thread().name
        # Add the file handler to the logger
        logger_.addHandler(debug_file_handler)
        logger_.debug("Debug file handler set to main thread")

        # Create FileHandler info file handler
        info_file_handler = logging.FileHandler(filename=f"{file_str}-FH-Info.log", mode='a')
        info_file_handler.setFormatter(clean_formatter)  # Set the formatter to only show the message
        info_file_handler.setLevel(logging.INFO)
        # Set the file handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        info_file_handler._lock = threading.Lock()
        info_file_handler._thread = threading.main_thread()
        info_file_handler._thread_id = threading.get_ident()
        info_file_handler._thread_name = threading.current_thread().name
        # Add the file handler to the logger
        logger_.addHandler(info_file_handler)
        logger_.debug("Debug file handler set to main thread")

        # Create info text handler
        text_handler = TextHandler(tkinter_text)
        text_handler.setFormatter(clean_formatter)  # Set the formatter to only show the message
        text_handler.setLevel("INFO")  # Set the level to DEBUG or INFO as needed
        # Set the file handler to use the same thread as the main thread
        # This is necessary because we can't modify the Text from other threads
        text_handler._lock = threading.Lock()
        text_handler._thread = threading.main_thread()
        text_handler._thread_id = threading.get_ident()
        text_handler._thread_name = threading.current_thread().name
        logger_.addHandler(text_handler)
        logger_.info("Info Text_handler added to log object")

    except Exception as ex:
        file_name = os.path.split(inspect.stack()[0][1])[1]
        function_name = inspect.stack()[0][3]
        message = f"{file_name} : {function_name} : An exception of type {type(ex)} occurred. Arguments:\n{ex.args}"
        print(message)
    finally:
        return logger_


def test():
    i = 0
    while i < 5:
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warning message')
        logger.error('error message')
        logger.critical('critical message')
        i += 1
        sleep(1)


# Sample usage
if __name__ == '__main__':
    # Create the GUI
    root = tkinter.Tk()
    
    import tkinter.scrolledtext as ScrolledText
    st = ScrolledText.ScrolledText(root, state='disabled')
    st.configure(font='TkFixedFont')
    st.pack()

    B = tkinter.Button(root, text ="Run test", command = test)
    B.place(x=50,y=50)
    # Create textLogger
    # text_handler = TextHandler(st)

    # Add the handler to logger
    # logger = logging.getLogger()
    # logger.addHandler(text_handler)
    logger = create_console_file_tkinter_logger("test", st)

    root.mainloop()

    # Log some messages
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')


