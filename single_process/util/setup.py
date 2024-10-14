# Installed Packages
import cv2

# Standard Packages
import os
from datetime import datetime

# Original Sources
from .yaml import read

class Manager:
    def __init__(self, config_path):
        self.config = read(config_path=config_path)

    def get_model_path(self):
        return self.config['model']
    
    def get_video_path(self):
        return self.config['video_path']

    def get_output_path(self):
        return self.config['video_output_path']

    def get_log_path(self):
        return self.config['log_path']