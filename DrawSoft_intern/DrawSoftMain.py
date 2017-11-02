import cv2
import os
import numpy as np
import datetime
from Elements import *
from StartScreen import *
import math
import multiprocessing
import time

class Screen():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1920//2)  # Width
        self.cap.set(4, 1080//2)  # Height
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

def drawLine(i, iCP, color, drawImg):
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
            cv2.circle(drawImg,(int(xsumtemp), int(ysumtemp)),int(i[2]/2), color, -1)
            j += 1

    cv2.circle(drawImg,(int(i[0]), int(i[1])),int(i[2]/2), color, -1)

def deleteLine(i, drawImg):
    cv2.circle(drawImg,(int(i[0]), int(i[1])),int(i[2]/2), (255,255,255), -1)

def parafunc(param):
    for x in range(Screen().width()):
        if(drawImg[param][x][0]!=255 or drawImg[param][x][1]!=255 or drawImg[param][x][2]!=255):
            for k in range(3):
                img[param][x][k] = drawImg[param][x][k]


def MainLoop():
    screen = Screen()

    global drawImg
    drawImg = np.tile(np.uint8([255, 255, 255]), (screen.height(), screen.width(), 1))
    print("draeimg : ",len(drawImg),len(drawImg[0]))
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
                            param1=50,param2=75,minRadius=60,maxRadius=150)

        if circles is not None:
            circles = np.int16(np.around(circles))
            for i in circles[0,:]:
                #お絵描きモード
                if state == "draw":
                    if iCP is None: iCP = i
                    drawLine(i,iCP,color,drawImg)
                #消しゴムモード
                else:
                    deleteLine(i, drawImg)
                iCP = i

        #画面合成(重すぎて動かないのでコメント化)

        start = time.time()
        pool = multiprocessing.Pool()
        pool.map(parafunc, range(screen.height()))
        """
        for y in range(screen.height()):
            for x in range(screen.width()):
                if(drawImg[y][x][0]!=255 or drawImg[y][x][1]!=255 or drawImg[y][x][2]!=255):
                    for k in range(3):
                        img[y][x][k] = drawImg[y][x][k]
        """
        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        

        #img = cv2.bitwise_and(img, drawImg)

        mode = "draw mode" if state == "draw" else "delete mode"
        cv2.putText(img, mode,(int(screen.width()-200),int(screen.height()-20)), fontType, 0.7, (0, 0, 0), 2, -1)
        cv2.imshow('DrawSoft',img)
        #cv2.imshow('drawImg',drawImg)

        key = cv2.waitKey(10)
        if key is ord('x'): drawImg = np.tile(np.uint8([255, 255, 255]), (screen.height(), screen.width(), 1))
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
    #StartScreen()
    MainLoop()