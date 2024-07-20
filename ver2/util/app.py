# Installed Libraries
import cv2
from ultralytics import YOLO
from motpy import Detection, MultiObjectTracker

class VideoDetector:
    def __init__(self, model_path, logger):
        self.model = YOLO(model_path)
        self.logger = logger
        self.detcection_targets = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck']
    
    def detectHuman(self, frame):
        try:
            detected = self.model(frame)
            boxes = detected[0].boxes
            target_count = {'person': 0, 'bicycle': 0, 'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}

            # self.logger.info(detected)

            for box in boxes:
                cls = box.cls
                conf = box.conf
                xyxy = box.xyxy

                target_name = self.model.names[int(cls)]

                if target_name in self.detcection_targets and conf >= 0.5:
                    frame = self.drawRectAngle(frame, xyxy)
                    target_count[target_name] += 1
                    self.logger.info([target_name, conf])

            
            frame = self.drawInfo(frame, target_count)

            return frame

        except cv2.error as e:
            print(e)
    
    def drawRectAngle(self, frame, xyxy):
        for _xyxy in xyxy:
            x1, y1, x2, y2 = map(int, _xyxy)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            center = ((x1+x2) // 2, (y1+y2) // 2)
            frame = self.drawCenterPoint(frame, center)

        return frame

    def drawCenterPoint(self, frame, center):
        frame = cv2.circle(frame, center, 2, (0, 255, 0), 3)
        
        return frame

    def drawInfo(self, frame, target_count):
        for i, (target, count) in enumerate(target_count.items()):
            text = f"{target.capitalize()}: {count}"
            cv2.putText(frame, text, (50, 100 + i * 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)

        # cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return frame