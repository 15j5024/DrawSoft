import cv2
import numpy as np
from DrawSoftMain import Screen

class StartScreen:
    def __init__(self):
        img_start = cv2.imread('DrawSoftStartScreen.png')
        startScreen = np.tile(np.uint8([255, 255, 255]), (Screen().height(), Screen().width(), 1))
        fontType = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(startScreen, 'push a',(int(Screen().width()/4),int(Screen().height()/2)), fontType, 10, (0, 0, 0), 20, -1)
        #cv2.imshow('DrawSoft',startScreen)
        cv2.imshow('DrawSoft',img_start)

        while True:
            key = cv2.waitKey(100)
            if key is ord('a'):
                break