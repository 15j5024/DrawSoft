import cv2
import os
import numpy as np
import datetime
from Elements import *
import math

class Screen():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    def height(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    def width(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

def make_dir():
    if not os.path.exists('.\\picture') :
        os.makedirs('.\\picture')
    else : 
        return None

def picture(img):
      d = datetime.datetime.today()
      faile = ".\\picture\\"
      name = faile+'%s-%s-%s-%s-%s-%s'%(d.year, d.month, d.day,d.hour,d.minute,d.second)+'.png'  
      cv2.imwrite(name,img)

def change_color(key):
    #黒
    c1,c2,c3 = 0,0,0
    #赤
    if key == ord('r'):
        c3 = 255
    #緑   
    if key == ord('g'):
        c2 = 255
    #青
    if key == ord('b'):
        c1 = 255 
    return (c1,c2,c3)

def keyInput(key):
    if key is ord('x'):
        circlelist = []

def drawLine(i, iCP,color):
    xsub = abs(i[0]-iCP[0])
    ysub = abs(i[1]-iCP[1])
    z = int(math.sqrt(xsub**2 + ysub**2))
    sub = int(z/5)

    if z > 10 and z < 80: 
        xsum =  iCP[0] + ( (i[0]-iCP[0]) / sub )
        ysum =  iCP[1] + ( (i[1]-iCP[1]) / sub )
        xtemp = xsum - iCP[0]
        ytemp = ysum - iCP[1]

        j=0
        while j < sub:
            xsumtemp = xsum + (xtemp * j)
            ysumtemp = ysum + (ytemp * j)
            ele = Elements()
            ele.setAll(int(xsumtemp), int(ysumtemp), i[2], color)
            circlelist.append(ele)
            j += 1

    ele = Elements()
    ele.setAll(i[0],i[1],i[2],color)
    circlelist.append(ele)

def deleteLine(i):
    j = 0
    while j < len(circlelist):
        xsub = abs(circlelist[j].x - i[0])
        ysub = abs(circlelist[j].y - i[1])
        #円の中心と絵の中心との距離
        z = math.sqrt(xsub**2 + ysub**2)
        #円の半径と絵の半径の和
        ijz = i[2]+circlelist[j].r

        if(z < ijz):
            circlelist.remove(circlelist[j])
        j += 1

def MainLoop():
    screen = Screen()
    screen.cap.set(3, 1920)  # Width
    screen.cap.set(4, 1080)  # Height
    global circlelist
    circlelist = []
    global state
    state = "draw"
    iCP = None
    color = (0,0,0)
    fontType = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        _, img = screen.cap.read()
        if img is None: break
        img = cv2.medianBlur(img,5)
        cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=75,minRadius=15,maxRadius=150)

        if circles is not None:
            circles = np.int16(np.around(circles))
            #print(circles)
            for i in circles[0,:]:
                #お絵描きモード
                if state == "draw":
                    if iCP is None: iCP = i
                    drawLine(i,iCP,color)
                #消しゴムモード
                else:
                    deleteLine(i)
                iCP = i

        #print (f'circlelist = {len(circlelist): 4d}', end='\r')

        j = 0 
        while j < len(circlelist):
            cv2.circle(img,(circlelist[j].x, circlelist[j].y),int(circlelist[j].r/2),circlelist[j].color,-1) 
            j += 1

        mode = "draw mode" if state == "draw" else "delete mode"
        cv2.putText(img, mode,(int(screen.width()-200),int(screen.height()-20)), fontType, 0.7, (0, 0, 0), 2, -1)
        cv2.imshow('DrawSoft',img)

        key = cv2.waitKey(10)
        if key is ord('x'): circlelist = []
        if key is ord('d'): state = "delete"
        if key is ord('w'): state = "draw"
        if(key is ord('r')
        or key is ord('g')
        or key is ord('b')
        or key is ord('k')): color=change_color(key)
        if key is ord('q'): picture(img)
        if key is ord('e'): break

    cv2.destroyAllWindows()
    screen.cap.release()

if __name__ == '__main__':
    make_dir()
    MainLoop()