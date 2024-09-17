# Standard Packages
import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_path):
        now = datetime.now().strftime("%Y-%m-%d")
        self.log_path = log_path.format(date=now)
    
    def setup_logger(self):

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(filename=self.log_path, mode='w')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
    
    def make_directory_log_path(self):
        log_dir = os.path.dirname(self.log_path)
        os.makedirs(name=log_dir, exist_ok=True)
    
    def get_logger(self):
        return self.logger