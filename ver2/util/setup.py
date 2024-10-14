# Installed Packages
import cv2

# Standard Packages
import os
from multiprocessing import Queue
from datetime import datetime

# Original Sources
from .yaml import read
from .log import Logger

def load_settings(config_path):
    config = read(config_path)

    return config


def set_up_cap(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(
            """
                VideoCapture not opened. \n
                Check if the 'movie_path' is correct and ffmpeg or gstreamer is properly installed.
            """
        )
    return cap


def set_up_queue():
    frame_queue = Queue()
    result_queue = Queue()
    log_queue = Queue()

    return frame_queue, result_queue, log_queue


def set_up_writer(cap, output_path):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (cap_width, cap_height))
    
    return writer

def set_up_logger(log_path, log_queue=None):
    # Get Date
    now = datetime.now().strftime("%Y-%m-%d")

    # Logfile Setting
    log_path = log_path.format(date=now)
    
    # Create Log Directory
    log_dir = os.path.dirname(log_path)
    os.makedirs(log_dir, exist_ok=True)

    # logger = Logger(log_path).get_logger()
    logger_manager = Logger(log_path, log_queue)

    return logger_manager

def set_up_csv(csv_path):
    csv_dir = os.path.dirname(csv_path)
    os.makedirs(csv_dir, exist_ok=True)