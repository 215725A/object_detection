# Installed Packages
import torch
import numpy as np

# Standard Packages
import argparse
import time
import logging
import gc
from logging.handlers import QueueHandler
from multiprocessing import Process

# Original Sources
import util.app as app
from util.setup import load_settings, set_up_cap, set_up_queue, set_up_writer, set_up_logger, set_up_csv_one_path
from util.mot import MOT
from util.csv import load_target_csv, load_ratio_csv, load_expect_area_csv


def process_detector(**option):
    frame_queue = option['frame_queue']
    result_queue = option['result_queue']
    model_path = option['model_path']
    log_queue = option['log_queue']
    target_area_points = option['target_area_points']
    aspect_ratio = option['aspect_ratio']
    expect_area = option['expect_area']

    logger = logging.getLogger()
    logger.addHandler(QueueHandler(log_queue))
    logger.setLevel(logging.DEBUG)

    detector = app.VideoDetector(model_path, logger, expect_area, aspect_ratio)
    detector.setPolygon(target_area_points)

    while True:
        frame_number, frame = frame_queue.get()
        if frame is None:
            break

        try:
            with torch.no_grad():
                detections, target_count, congestion_rate = detector.detectObject(frame)
        except RuntimeError as e:
            logger.error(f"RuntimeError: {e}")
            continue
        
        result_queue.put((frame_number, frame, detections, target_count, congestion_rate)) 
        
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
    target_area_points_path = config['target_area_points_output_path']
    aspect_ratio_path = config['aspect_ratio_output_path']
    expect_area_path = config['expect_area_output_path']
    congestion_rate_path = config['congestion_rate_output_path']

    # Setup
    cap = set_up_cap(video_path)
    frame_queue, result_queue, log_queue = set_up_queue()
    writer = set_up_writer(cap, output_path)
    set_up_csv_one_path(congestion_rate_path)

    # Load csv Files
    target_area_points = load_target_csv(target_area_points_path)
    aspect_ratio = load_ratio_csv(aspect_ratio_path)
    expect_area = load_expect_area_csv(expect_area_path)

    # Setup Multi Object Tracker
    tracker = MOT(dt=0.1)

    # Setup Logger
    logger_manager = set_up_logger(log_path, log_queue)
    logger_manager.setup_logger()
    logger_manager.start_listener()

    option = {
        "frame_queue": frame_queue, 
        "result_queue": result_queue, 
        "model_path": model_path, 
        "log_queue": log_queue,
        "target_area_points": target_area_points,
        "aspect_ratio": aspect_ratio,
        "expect_area": expect_area
    }

    # Setup Workers
    detectors = [
        Process(target=process_detector, kwargs=(option))
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
    congestion_rates = [None] * frame_number
    for _ in range(frame_number):
        frame_number, frame, detections, target_count, congestion_rate = result_queue.get()
        tracks = tracker.update(detections)

        for track in tracks:
            track_id = track.id
            xyxy = track.box
            color = tracker.get_color(track_id)

            frame = app.VideoDetector.drawRectAngle(frame, color, xyxy)
            # frame = app.VideoDetector.drawTrackID(frame, track_id, xyxy)
            frame = app.VideoDetector.drawInfo(frame, target_count)
        frames[frame_number] = frame
        congestion_rates[frame_number] = congestion_rate
    
    np.savetxt(congestion_rate_path, congestion_rates, delimiter=',', fmt='%.5f')
    
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
