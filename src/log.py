import logging
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("myapp") # need to check why necessery. does it need to by inside setup_logging?

def setup_logging():
    logger.setLevel(logging.DEBUG) 
    formatter = logging.Formatter("%(asctime)s %(levelname)s\t%(filename)s - %(funcName)s - %(message)s") 

    file_handler = RotatingFileHandler("my_log.log", maxBytes=100000, backupCount=3) # need to understand all parts of it
    print_handler = logging.StreamHandler(sys.stdout) 
    print_handler.setLevel(logging.INFO) 
    file_handler = logging.FileHandler("logs/my.log") # need to check why necessery
    print_handler.setLevel(logging.DEBUG) 
    file_handler.setFormatter(formatter) 

    if not logger.handlers:
        logger.addHandler(print_handler)
        logger.addHandler(file_handler)