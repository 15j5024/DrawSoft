import cv2
import numpy as np

class Elements:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 0
        self.color = (0,0,0)
    
    def setAll(self,x2,y2,r2,color2):
        self.x = x2
        self.y = y2
        self.r = r2
        self.color = color2



