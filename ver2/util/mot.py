# Installed Packages
from motpy import MultiObjectTracker

# Standard Packages
import random

class MOT:
    def __init__(self, dt=0.1):
        self.tracker = MultiObjectTracker(dt=dt, tracker_kwargs={'max_staleness': 60})
        self.colors = {}
    
    def update(self, detections):
        self.tracker.step(detections=detections)
        return self.tracker.active_tracks()
    
    def get_color(self, track_id):
        if track_id not in self.colors:
            # Generate Random Color
            self.colors[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        return self.colors[track_id]