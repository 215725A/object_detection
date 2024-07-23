# Installed Packages
from motpy import MultiObjectTracker

# Standard Packages
import random

class MOT:
    def __init__(self, dt=0.1):
        self.tracker = MultiObjectTracker(dt=dt, tracker_kwargs={'max_staleness': 10})
        self.coloers = {}
    
    def update(self, detections):
        self.tracker.step(detections=detections)
        return self.tracker.active_tracks()
    
    def get_color(self, track_id):
        if track_id not in self.coloers:
            # Generate Random Coloer
            self.coloers[track_id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        return self.coloers[track_id]