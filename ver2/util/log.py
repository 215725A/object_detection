# Standard Packages
import logging
from logging import FileHandler
import logging.handlers
from logging.handlers import QueueHandler, QueueListener
import multiprocessing
from multiprocessing import Queue

class Logger:
    def __init__(self, log_path, log_queue):
        self.log_queue = log_queue
        self.log_path = log_path

    
    def setup_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(QueueHandler(self.log_queue))
    
    def start_listener(self):
        file_handler = FileHandler(self.log_path, mode='w')
        file_handler.setFormatter(logging.Formatter("%(levelname)-9s %(message)s"))
        self.listener = QueueListener(self.log_queue, file_handler)
        self.listener.start()
    
    def stop_listener(self):
        self.listener.stop()