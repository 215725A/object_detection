# Installed Libraries
import cv2
from ultralytics import YOLO
from motpy import Detection, MultiObjectTracker

class VideoDetector:
    def __init__(self, model_path, logger):
        self.model = YOLO(model_path)
        self.logger = logger
    
    def detectHuman(self, frame):
        try:
            detected = self.model(frame)
            boxes = detected[0].boxes
            human_count = 0

            self.logger.info(detected)

            for box in boxes:
                cls = box.cls
                conf = box.conf
                xyxy = box.xyxy

                if self.model.names[int(cls)] == 'person' and conf >= 0.5:
                    frame = self.drawRectAngle(frame, conf, xyxy)
                    human_count += 1
            
            frame = self.drawInfo(frame, human_count)

            return frame

        except cv2.error as e:
            print(e)
    
    def drawRectAngle(self, frame, conf, xyxy):
        for _xyxy, _conf in zip(xyxy, conf):
            x1, y1, x2, y2 = map(int, _xyxy)
            label = f'person: {_conf:.2f}'

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            center = ((x1+x2) // 2, (y1+y2) // 2)
            frame = self.drawCenterPoint(frame, center)

        return frame

    def drawCenterPoint(self, frame, center):
        frame = cv2.circle(frame, center, 2, (0, 255, 0), 3)
        
        return frame

    def drawInfo(self, frame, human_count):
        text = f"Human: {human_count}"
        cv2.putText(frame, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return frame