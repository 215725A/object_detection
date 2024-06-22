# Installed Libraly
import cv2
from ultralytics import YOLO

# Self-made Libraly
from . import yaml

class VideoDetector:
    def __init__(self):
        self.cneter_points = []

    def setupVideoCapture(self):
        video_path = self.config['video_path']
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError("""
                             VideoCapture not opened. \n
                             Check if the 'movie_path' is correct and ffmpeg or gstreamer is properly installed.
                            """
            )
        self.cap_witdh = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cap_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
    
    def setupVideoWriter(self):
        output_path = self.config['video_output_path']
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(output_path, self.fourcc, self.fps, (self.cap_witdh, self.cap_height))
    
    def setupModel(self):
        model = self.config['model']
        self.model = YOLO(model)

    def release(self):
        self.writer.release()
        self.cap.release()
        cv2.destroyAllWindows()

    def detectHumanBody(self):
        try:
            while self.cap.isOpened():
                ret, self.frame = self.cap.read()

                if not ret:
                    break

                detected = self.model(self.frame)
                boxes = detected[0].boxes

                for box in boxes:
                    cls = box.cls
                    conf = box.conf
                    xyxy = box.xyxy
                
                    if self.model.names[int(cls)] == 'person' and conf >= 0.5:
                        self.drawRectAngle(conf, xyxy)

                self.saveVideo(self.frame)

        except cv2.error as e:
            print(e)
        
        self.release()

    def drawRectAngle(self, conf, xyxy):
        for _xyxy, _conf in zip(xyxy, conf):
            x1, y1, x2, y2 = map(int, _xyxy)
            label = f'person: {_conf:.2f}'
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(self.frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            # self.drawCenterPoint(center_x, center_y)
            self.drawObit((center_x, center_y))

    # def drawCenterPoint(self, center_x, center_y):
    #     cv2.circle(self.frame, (center_x, center_y), 2, (0, 255, 0), 3)
    
    def drawObit(self, new_center_point):
        self.cneter_points.append(new_center_point)
        for points in self.cneter_points:
            cv2.circle(self.frame, points, 2, (0, 255, 0), 3)

    def saveVideo(self, frame):
        self.writer.write(frame)

    def roadConfigFile(self, file_path):
        config_path = f'{file_path}'
        self.config = yaml.read(config_path)