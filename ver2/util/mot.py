# Installed Packages
from motpy import MultiObjectTracker, Detection
import torch

# Standard Packages
import random

class MOT:
    def __init__(self, dt=0.1):
        self.tracker = MultiObjectTracker(dt=dt, tracker_kwargs={'max_staleness': 10})
        self.coloers = {}
    
    def update(self, detections):
        cpu_detections = self.convert_to_cpu(detections)
        self.tracker.step(detections=cpu_detections)
        return self.tracker.active_tracks()
    
    def get_color(self, track_id):
        if track_id not in self.coloers:
            # Generate Random Coloer
            self.coloers[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        return self.coloers[track_id]
    
    def convert_to_cpu(self, detections):
        cpu_detections = []
        for detection in detections:
            # `detection.box` が `torch.Tensor` かどうかを確認
            if isinstance(detection.box, torch.Tensor):
                box = detection.box.cpu().tolist()
            elif isinstance(detection.box, list):
                box = detection.box
            else:
                raise TypeError(f"Unexpected type for detection.box: {type(detection.box)}")

            # `detection.score` が `torch.Tensor` かどうかを確認
            if isinstance(detection.score, torch.Tensor):
                score = detection.score.cpu().item()
            else:
                score = detection.score

            cpu_detections.append(Detection(box=box, score=score))
        return cpu_detections