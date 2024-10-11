import cv2

class Area:
    def __init__(self, frame):
        self.img = frame
        self.wname = "Select Load Points"
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

    def calcArea(self):
        n = len(self.point_list)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.point_list[i][0] * self.point_list[j][1]
            area -= self.point_list[j][0] * self.point_list[i][1]
        area = abs(area) / 2.0
        return area