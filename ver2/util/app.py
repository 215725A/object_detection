# Installed Packages
import cv2
import torch
import numpy as np
from ultralytics import YOLO
from motpy import Detection
from shapely.geometry import Polygon

# Original Sources

class VideoDetector:
    def __init__(self, model_path, logger, expect_area, aspect_ratio):
        if torch.cuda.is_available():
            self.model = YOLO(model_path).to('cuda')
        else:
            self.model = YOLO(model_path)
        self.logger = logger
        self.detection_targets = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck']
        self.expect_area = expect_area
        self.aspect_ratio = aspect_ratio
        

    def setPolygon(self, target_area_points):
        self.polygon_points = np.array(target_area_points)
        self.polygon = Polygon(self.polygon_points)
    
    def detectObject(self, frame):
        try:
            with torch.no_grad():
                detected = self.model(frame)
            
            boxes = detected[0].boxes
            target_count = {'person': 0, 'bicycle': 0, 'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}
            detections = []
            total_area = 0

            horizontal_ratio = self.aspect_ratio[0][0]
            vertical_ratio = self.aspect_ratio[1][0]

            for box in boxes:
                cls = box.cls
                conf = box.conf
                xyxy = box.xyxy[0]

                target_name = self.model.names[int(cls)]

                if target_name in self.detection_targets and conf >= 0.5:
                    # frame = self.drawRectAngle(frame, xyxy)
                    x1, y1, x2, y2 = xyxy

                    bounding_box = [
                                    (x1, y1), 
                                    (x2, y1), 
                                    (x2, y2), 
                                    (x1, y2)
                                    ]

                    bounding_box_polygon = Polygon(bounding_box)

                    intersection_area = self.polygon.intersection(bounding_box_polygon).area
                    total_area += intersection_area

                    bbox = list(map(float, (x1, y1, x2, y2)))
                    detection = Detection(box=bbox, score=conf)
                    detections.append(detection)

                    target_count[target_name] += 1
                    self.logger.info([target_name, conf])

            total_area *= vertical_ratio * horizontal_ratio
            congestion_rate = (total_area / self.expect_area) * 100

            return detections, target_count, congestion_rate

        except cv2.error as e:
            print(e)
    
    def withInRangeTargetPoints(self, target_points):
        pass
    
    @classmethod
    def drawInfo(cls, frame, target_count):
        for i, (target, count) in enumerate(target_count.items()):
            text = f"{target.capitalize()}: {count}"
            cv2.putText(frame, text, (50, 100 + i * 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)

        return frame
    
    @classmethod
    def drawRectAngle(cls, frame, color, xyxy):
        # for _xyxy in xyxy:
        x1, y1, x2, y2 = map(int, xyxy)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        center = ((x1+x2) // 2, (y1+y2) // 2)
        frame = cls.drawCenterPoint(frame, center)

        return frame

    @classmethod
    def drawCenterPoint(cls, frame, center):
        frame = cv2.circle(frame, center, 2, (0, 255, 0), 3)
        
        return frame

    @classmethod
    def drawTrackID(cls, frame, track_id, xyxy):
        x1, y1, _, _ = map(int, xyxy)
        frame = cv2.putText(frame, f'ID: {track_id}', (x1, (y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        return frame