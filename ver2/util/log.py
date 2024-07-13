# Standard Packages
import logging
from logging import FileHandler

class Logger:
    def __init__(self, log_path):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)-9s %(message)s",
            datefmt="[%X]",
            handlers=[FileHandler(filename=log_path, mode='w')]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_logger(self):
        return self.logger