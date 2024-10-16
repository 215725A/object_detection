# Installed Packages
import cv2
import torch
from ultralytics import YOLO
from .mot import MOT
from motpy import Detection
from motpy.testing_viz import draw_track

# Standard Packages
import os

class Detector:
    def __init__(self, model_path, logger):
        if torch.cuda.is_available():
            self.model = YOLO(model=model_path).to('cuda')
        else:
            self.model = YOLO(model=model_path)
        
        self.detcection_targets = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck']

        self.logger = logger

        self.tracker = MOT(dt=0.1)

        self.writer = None
    
    def setup_video(self, video_path):
        self.cap = cv2.VideoCapture(filename=video_path)
        if not self.cap.isOpened():
            raise ValueError(
                """
                    VideoCapture not opened. \n
                    Check if the 'movie_path' is correct and ffmpeg or gstreamer is properly installed.
                """
            )

    def setup_writer(self, output_file):
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        cap_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        cap_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(filename=output_file, fourcc=fourcc, fps=fps, frameSize=(cap_width, cap_height))

        if not self.writer.isOpened():
            raise ValueError(f"VideoWriter not opened. Output file: {output_file}, Codec: {fourcc}, FPS: {fps}, Width: {cap_width}, Height: {cap_height}")

    def start_detect(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            try:
                with torch.no_grad():
                    detected = self.model(frame)

                boxes = detected[0].boxes
                target_count = { target_name: 0 for target_name in self.detcection_targets }
                detections = []

                for box in boxes:
                    cls = box.cls
                    conf = box.conf
                    xyxy = box.xyxy[0]

                    target_name = self.model.names[int(cls)]

                    if target_name in self.detcection_targets and conf >= 0.5:
                        x1, y1, x2, y2 = xyxy
                        bbox = list(map(float, (x1, y1, x2, y2)))
                        detection = Detection(box=bbox, score=conf, class_id=int(cls))
                        detections.append(detection)

                        target_count[target_name] += 1
                        self.logger.info([target_name, conf])
                
                tracks = self.tracker.update(detections=detections)

                for track in tracks:
                    draw_track(frame, track, thickness=1)
                
                self.writer.write(frame)

            except cv2.error as e:
                raise(e)

        self.writer.release()
        self.cap.release() 