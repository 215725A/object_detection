# Installed Packages
import cv2
import torch

# Standard Packages
import argparse
import time
import logging
import gc
from logging.handlers import QueueHandler
from multiprocessing import Process

# Original Sources
import util.app as app
import util.area as area
from util.setup import load_settings, set_up_cap, set_up_queue, set_up_writer, set_up_logger
from util.mot import MOT


def main(config_path):
  start = time.perf_counter()

  # Load Settings
  model_path, video_path, output_path, _, log_path = load_settings(config_path)

  detector = app.VideoDetector(model_path)

  cap = set_up_cap(video_path)

  end = time.perf_counter()

  print(f"実行時間: {end - start:.2f}s")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)