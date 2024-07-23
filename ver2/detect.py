# Installed Packages
import cv2

# Standard Packages
import argparse
import time
import logging
from logging.handlers import QueueHandler
import multiprocessing
from multiprocessing import Process, Queue

# Original Sources
import util.app as app
from util.setup import load_settings, set_up_cap, set_up_queue, set_up_writer, set_up_logger


def process_detector(frame_queue, result_queue, model_path, log_queue):
    logger = logging.getLogger()
    logger.addHandler(QueueHandler(log_queue))
    logger.setLevel(logging.DEBUG)

    detector = app.VideoDetector(model_path, logger)

    while True:
        frame_number, frame = frame_queue.get()
        if frame is None:
            break

        result = detector.detectHuman(frame)
        result_queue.put((frame_number, result)) 

def save_video(writer, results):
    if results:
        for frame in results:
            writer.write(frame)
        writer.release()

def main(config_path):
    start = time.perf_counter()

    # Load Settings
    model_path, video_path, output_path, process_num, log_path = load_settings(config_path)

    # Setup
    cap = set_up_cap(video_path)
    frame_queue, result_queue, log_queue = set_up_queue()
    writer = set_up_writer(cap, output_path)

    # Setup Logger
    logger_manager = set_up_logger(log_path, log_queue)
    logger_manager.setup_logger()
    logger_manager.start_listener()

    # Setup Workers
    detectors = [
        Process(target=process_detector, args=(frame_queue, result_queue, model_path, log_queue))
        for _ in range(process_num)
    ]

    for detector in detectors:
        detector.start()
    
    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put((frame_number, frame))
        frame_number += 1
    
    for _ in detectors:
        frame_queue.put((None, None))
    
    frames = [None] * frame_number
    for _ in range(frame_number):
        frame_number, result = result_queue.get()
        frames[frame_number] = result
    
    for detector in detectors:
        detector.join()

    save_video(writer, frames)

    cap.release()
    writer.release()

    logger = logging.getLogger()
    logger.addHandler(QueueHandler(log_queue))
    logger.setLevel(logging.DEBUG)
    logger.warning("All process finished!")

    logger_manager.stop_listener()

    end = time.perf_counter()
    print(f"実行時間: {end - start:.2f}s")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)
