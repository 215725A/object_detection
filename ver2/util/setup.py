# Installed Packages
import cv2

# Standard Packages
from multiprocessing import Queue

# Original Sources
from .yaml import read

def load_settings(config_path):
    config = read(config_path)
    model_path = config['model']
    video_path = config['video_path']
    output_path = config['video_output_path']
    process_num = config['process_num']

    return model_path, video_path, output_path, process_num


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

    return frame_queue, result_queue


def set_up_writer(cap, output_path):
    cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (cap_width, cap_height))
    
    return writer