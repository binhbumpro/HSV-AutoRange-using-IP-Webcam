import cv2
import numpy as np
from Mobile_Capture import Moble_capture

class Color_ranger:
    def __init__(self, image):
        self.image = image
        # self.hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        # self.hsv = cv2.blur(self.hsv, (5, 5))
        self.lower = [255,255,255]
        self.upper = [0,0,0]

    def range_grow(self, current):
        for i in range(0, 3):
            if self.lower[i] > current[i]:
                self.lower[i] = current[i]
            if self.upper[i] < current[i]:
                self.upper[i] = current[i]

    def box_click(self, event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            mouseX, mouseY = x, y
            current = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)[y][x]
            if self.lower is None and self.upper is None:
                self.lower = np.array([current[0], current[1], current[2]])
                self.upper = np.array([current[0], current[1], current[2]])
                return

            self.range_grow(current)
            self.show_mask()

    def balance_box(self, width, height):
        box_image = np.zeros((height, width, 3), np.uint8)
        balance = (np.array(self.upper) + np.array(self.lower)) / 2
        balance = np.uint8([[balance]])
        rgb_balance = cv2.cvtColor(balance, cv2.COLOR_HSV2RGB);

        rgb_balance = np.uint8(rgb_balance[0][0])
        cv2.rectangle(box_image, (0, 0), (width, height),
                      (int(rgb_balance[0]), int(rgb_balance[1]), int(rgb_balance[2])), -1)
        cv2.imshow('box', box_image)

    def show_mask(self):
        mask = cv2.inRange(cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV), np.array(self.lower), np.array(self.upper))

        cv2.putText(self.image, 'Lower : ' + str(self.lower), (10, 60), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(self.image, 'Upper : ' + str(self.upper), (10, 80), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1,
                    cv2.LINE_AA)
        print("Lower : {}\nUpper : {}\n---------------\n".format(self.lower, self.upper))
        # self.balance_box(150,50)
        cv2.imshow('mask', mask)
        cv2.imshow('image', self.image)



capture = Moble_capture('http://192.168.42.129:8080')
image = capture.get_image((640,480))
ranger = Color_ranger(capture.get_image())


ranger.image = image
while (1):
    image = capture.get_image((640,480))
    ranger.image = image.copy()

    cv2.setMouseCallback('image', ranger.box_click)
    cv2.setMouseCallback('mask', ranger.box_click)

    ranger.show_mask()

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

