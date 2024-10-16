import cv2
import numpy as np

class Area:
    def __init__(self, frame):
        self.img = frame
        self.wname = "Select Road Points"
        self.point_list = []
        self.point_num = 4
        self.params = {
            "img": self.img,
            "wname": self.wname,
            "point_list": self.point_list,
            "point_num": self.point_num
        }
    
    def drawArea(self):
        if self.img is None:
            print("Error: Image not loaded properly.")
            return

        cv2.namedWindow(self.wname)
        cv2.setMouseCallback(self.wname, self.onMouse, self.params)
        while True:
            display_img = self.img.copy()
            for i in range(len(self.point_list)):
                cv2.circle(display_img, (self.point_list[i][0], self.point_list[i][1]), 3, (0, 0, 255), 3)
                if 0 < i:
                    cv2.line(display_img, (self.point_list[i][0], self.point_list[i][1]), (self.point_list[i-1][0], self.point_list[i-1][1]), (0, 255, 0), 2)
                if i == self.point_num - 1:
                    cv2.line(display_img, (self.point_list[i][0], self.point_list[i][1]), (self.point_list[0][0], self.point_list[0][1]), (0, 255, 0), 2)
            if 0 < len(self.point_list) < self.point_num:
                cv2.line(display_img, (self.point_list[-1][0], self.point_list[-1][1]), (self.point_list[-1][0], self.point_list[-1][1]), (0, 255, 0), 2)
            
            cv2.imshow(self.wname, display_img)
            key = cv2.waitKey(1)
            if key == 13:  # Enter key is pressed
                if len(self.point_list) == self.point_num:
                    cv2.destroyAllWindows()
                    break
                else:
                    print("Please select exactly 4 points before pressing Enter.")

        return display_img

    def onMouse(self, event, x, y, flags, params):
        point_list = params['point_list']
        point_num = params['point_num']

        # 左クリックでポイント追加
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(point_list) < point_num:
                point_list.append([x, y])
        
        # 右クリックでポイント削除
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(point_list) > 0:
                point_list.pop(-1)

    def calcArea(self, expect_distances):
        n = len(expect_distances)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += expect_distances[i][0] * expect_distances[j][1]
            area -= expect_distances[j][0] * expect_distances[i][1]
        area = abs(area) / 2.0
        return area
    
    def applyProjectiveTransform(self, target_points, selected_points):
        road_points_1 = np.array(selected_points, dtype=np.float32)

        target_x= min(selected_points, key=lambda x: x[0])[0]

        road_points_2 = np.array([(target_x, target_points[0]), (target_x, 0), (target_points[1], 0), (target_points[1], target_points[0])], dtype=np.float32)

        M = cv2.getPerspectiveTransform(road_points_1, road_points_2)
        np.set_printoptions(precision=5, suppress=True)

        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        w, h = road_points_2.max(axis=0).astype(int) + 50
        self.convert_img = cv2.warpPerspective(img, M, (w, h))

        cv2.imshow('Convert Image', self.convert_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return road_points_2

    def calcAspectRatio(self, expect_distances):
        expect_vertical, expect_horizontal = expect_distances
        min_x = min(self.point_list, key=lambda x: x[0])[0]
        max_x = max(self.point_list, key=lambda x: x[0])[0]
        x_length_data = max_x - min_x

        min_y = min(self.point_list, key=lambda x: x[1])[1]
        max_y = max(self.point_list, key=lambda x: x[1])[1]
        y_length_data = max_y - min_y

        x_ratio = expect_horizontal / x_length_data
        y_ratio = expect_vertical / y_length_data

        return [x_ratio, y_ratio]