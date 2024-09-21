# Installed Packages
import cv2
import numpy as np

# Standard Packages
import time

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
    
    def drawAreaAndCalcArea(self):
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

        # area = self.calcArea()
        # return area

    def onMouse(self, event, x, y, flags, params):
        point_list = params['point_list']
        point_num = params['point_num']

        # 左クリックでポイント追加
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(point_list) < point_num:
                point_list.append([x, y])
                print(f'Points: {[x, y]}')
        
        # 右クリックでポイント削除
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(point_list) > 0:
                point_list.pop(-1)

    def calcArea(self, points):
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        area = abs(area) / 2.0
        return area
    
    def applyProjectiveTransform(self):
        if len(self.point_list) < self.point_num:
            raise Exception("The point_list must have 4 coordinates.")

        road_points_1 = np.array(self.point_list, dtype=np.float32)
        # 基準とする道路四隅の実際の座標（単位cm）
        # road_points_2 = np.array([(53, 16500), (53, 0), (1478, 0), (1478, 16500)], dtype=np.float32)
        road_points_2 = np.array([(0, 0), (0, self.img.shape[0]), (self.img.shape[1], self.img.shape[0]), (self.img.shape[1], 0)], dtype=np.float32)

        M = cv2.getPerspectiveTransform(road_points_1, road_points_2)
        np.set_printoptions(precision=5, suppress=True)

        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        w, h = road_points_2.max(axis=0).astype(int) + 50
        self.convert_img = cv2.warpPerspective(img, M, (w, h))

        cv2.imshow('Convert Img', self.convert_img)
        cv2.waitKey(0)
        cv2.imwrite('outputs/img/car_1/convert_img.png', self.convert_img)
        cv2.destroyAllWindows()
    
    def checkLineLength(self):
        points = []
        params = {
            "img": self.convert_img,  # 操作用にコピーを作成
            "points": points
        }
        cv2.destroyAllWindows()
        time.sleep(2)
        
        cv2.namedWindow('Check')
        cv2.setMouseCallback('Check', self.onCheckEvent, params)

        while True:
            display_img = self.convert_img.copy()
            for i in range(len(points)):
                cv2.circle(display_img, (points[i][0], points[i][1]), 3, (0, 0, 255), 3)
                if 0 < i:
                    cv2.line(display_img, (points[i][0], points[i][1]), (points[i-1][0], points[i-1][1]), (0, 255, 0), 2)
                if i == self.point_num - 1:
                    cv2.line(display_img, (points[i][0], points[i][1]), (points[0][0], points[0][1]), (0, 255, 0), 2)
            if 0 < len(points) < self.point_num:
                cv2.line(display_img, (points[-1][0], points[-1][1]), (points[-1][0], points[-1][1]), (0, 255, 0), 2)
            
            cv2.imshow('Check', display_img)
            key = cv2.waitKey(1)
            if key == 13:  # Enter key is pressed
                if len(points) == self.point_num:
                    cv2.destroyAllWindows()
                    break
                else:
                    print("Please select exactly 4 points before pressing Enter.")

        area = self.calcArea(points)
        print(area)
        return area

    def onCheckEvent(self, event, x, y, flags, params):
        point_list = params['points']
        point_num = self.point_num

        # 左クリックでポイント追加
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(point_list) < point_num:
                point_list.append([x, y])
                print(f'White Line points: {[x, y]}')
        
        # 右クリックでポイント削除
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(point_list) > 0:
                point_list.pop(-1) # 画像に点を描画
