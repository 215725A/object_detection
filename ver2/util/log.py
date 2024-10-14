# Standard Packages
import logging
from logging import FileHandler
import logging.handlers
from logging.handlers import QueueHandler, QueueListener
import multiprocessing
from multiprocessing import Queue

class Logger:
    def __init__(self, log_path, log_queue=None):
        if log_queue is not None:
            self.log_queue = log_queue
        else:
            self.log_queue = None
        
        self.log_path = log_path


    def setup_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        if self.log_queue:
            self.logger.addHandler(QueueHandler(self.log_queue))


    def start_listener(self):
        file_handler = FileHandler(self.log_path, mode='w')
        file_handler.setFormatter(logging.Formatter("%(levelname)-9s %(message)s"))

        if self.log_queue is not None:
            self.listener = QueueListener(self.log_queue, file_handler)
            self.listener.start()

    def stop_listener(self):
        self.listener.stop()