# Installed Packages
import cv2
import torch

# Standard Packages
import argparse
import time
import logging
import gc

# Original Sources
from util.setup import *
from util.detector import Detector
from util.logger import Logger


def main(args):
    config_path = args.config

    # Initialize Start Time
    start_time = time.perf_counter()

    # Load Settings
    manager = Manager(config_path=config_path)
    model_path = manager.get_model_path()
    video_path = manager.get_video_path()
    output_path = manager.get_output_path()
    log_path = manager.get_log_path()

    # Setup Logger
    logger_manager = Logger(log_path=log_path)
    logger_manager.make_directory_log_path()
    logger_manager.setup_logger()
    logger = logger_manager.get_logger()

    # Setup Video Capture & Writer
    detector = Detector(model_path=model_path, logger=logger)
    detector.setup_video(video_path=video_path)
    detector.setup_writer(output_file=output_path)

    detector.start_detect()

    end_time = time.perf_counter()

    print(f'実行時間: {end_time - start_time:.2f}s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML File')

    args = parser.parse_args()

    main(args)