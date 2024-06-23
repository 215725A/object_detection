# Installed Libraries
import cv2

# Standard Libraries
import argparse
import time
from multiprocessing import Process, Queue

# Self-made Libraries
import util.app as app
from util.yaml import read


def process_detector(frame_queue, result_queue, model_path):
    detector = app.VideoDetector(model_path)
    while True:
        frame_number, frame = frame_queue.get()
        if frame is None:
            break

        result = detector.detectHuman(frame)
        result_queue.put((frame_number, result))

def load_settings(config_path):
    config = read(config_path)
    process_num = config['process_num']
    model_path = config['model']
    video_path = config['video_path']
    output_path = config['video_output_path']

    return process_num, model_path, video_path, output_path

def setUpCap(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("""
                             VideoCapture not opened. \n
                             Check if the 'movie_path' is correct and ffmpeg or gstreamer is properly installed.
                            """
        )

    return cap

def setUpQueue():
    frame_queue = Queue()
    result_queue = Queue()
    return frame_queue, result_queue

def setUpWriter(cap, output_path):
    cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (cap_width, cap_height))
    return writer

def saveVideo(writer, results):
    if results:
        for frame in results:
            writer.write(frame)
        writer.release()

def main(config_path):
    start = time.perf_counter()

    # Settings
    process_num, model_path, video_path, output_path = load_settings(config_path)

    # Setup
    cap = setUpCap(video_path)
    frame_queue, result_queue = setUpQueue()
    writer = setUpWriter(cap, output_path)

    # Setup Workers
    detectors = [
        Process(target=process_detector, args=(frame_queue, result_queue, model_path))
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
    
    results = [None] * frame_number
    for _ in range(frame_number):
        frame_number, result = result_queue.get()
        results[frame_number] = result
    
    for detector in detectors:
        detector.join()
    
    cap.release()

    saveVideo(writer, results)

    end = time.perf_counter()
    print(f"実行時間: {end - start:.2f}s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)
