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


def process_detector(frame_queue, result_queue, model_path, log_queue):
    logger = logging.getLogger()
    logger.addHandler(QueueHandler(log_queue))
    logger.setLevel(logging.DEBUG)

    detector = app.VideoDetector(model_path, logger)

    while True:
        frame_number, frame = frame_queue.get()
        if frame is None:
            break

        try:
            with torch.no_grad():
                detections, target_count = detector.detectHuman(frame)
        except RuntimeError as e:
            logger.error(f"RuntimeError: {e}")
            continue
        
        result_queue.put((frame_number, frame, detections, target_count)) 
        
        torch.cuda.empty_cache()
        gc.collect()

def save_video(writer, results):
    if results:
        for frame in results:
            writer.write(frame)
        writer.release()

def main(config_path):
    start = time.perf_counter()

    # Load Settings
    config = load_settings(config_path)
    model_path = config['model']
    video_path = config['video_path']
    output_path = config['video_output_path']
    log_path = config['log_path']
    process_num = config['process_num']

    # Setup
    cap = set_up_cap(video_path)
    frame_queue, result_queue, log_queue = set_up_queue()
    writer = set_up_writer(cap, output_path)

    # Setup Multi Object Tracker
    tracker = MOT(dt=0.1)

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
        frame_number, frame, detections, target_count = result_queue.get()
        tracks = tracker.update(detections)

        for track in tracks:
            track_id = track.id
            xyxy = track.box
            color = tracker.get_color(track_id)

            frame = app.VideoDetector.drawRectAngle(frame, color, xyxy)
            # frame = app.VideoDetector.drawTrackID(frame, track_id, xyxy)
            frame = app.VideoDetector.drawInfo(frame, target_count)
        frames[frame_number] = frame
    
    cap.release()

    for detector in detectors:
        detector.join()

    save_video(writer, frames)

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