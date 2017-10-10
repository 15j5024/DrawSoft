"""Detects lines in captured images using Hough-Transform."""
#! python3

import cv2
import os
import numpy as np
import datetime
from Elements import *
import math


#pictureフォルダの作成
def make_dir():
    if not os.path.exists('.\\picture') :
        os.makedirs('.\\picture')
    else : 
        return None


def picture(img):
      d=datetime.datetime.today()
      faile=".\\picture\\"
      name=faile+'%s-%s-%s-%s-%s-%s'%(d.year, d.month, d.day,d.hour,d.minute,d.second)+'.png'  

      cv2.imwrite(name,img)


def change_color(key):
    c1,c2,c3 = 0,0,0
    #色設定　赤
    if key == ord('r'):
        c3 = 255
    #色設定　緑   
    if key == ord('g'):
        c2 = 255
    #色設定　青
    if key == ord('b'):
        c1 = 255
    #色設定 黒    
    if key == ord('k'):  
        c1 = 0  
        c2 = 0  
        c3 = 0  

    return (c1,c2,c3)

def deleteCircles(circlelist,ele):
    j = 0
    while j < len(circlelist):
        xsub = abs(circlelist[j].x - ele.x)
        ysub = abs(circlelist[j].y - ele.y)
        z = math.sqrt(xsub**2 + ysub**2)
        if(z < int(ele.r)):
            circlelist.remove(circlelist[j])
        j += 1

def detect_line_segments_demo():
    cap = cv2.VideoCapture(0)
    flag = False
    circlelist = []
    r,g,b = (0,0,0)
    iCP = None
    drow =  True
    color = (0,0,0) 

    while True:
        _, img = cap.read()
        if img is None:
            break
        img = cv2.medianBlur(img,5)
        cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=75,minRadius=15,maxRadius=150)

        if (circles is None) and (flag == False):
            pass
        else:
            flag = True
            if (circles is not None):
                circles = np.int16(np.around(circles))
                for i in circles[0,:]:
                    
                    if iCP is None:
                        iCP = i

                    #circle同士が若干離れていたら間にcircleを距離に応じて入れる
                    xsub=abs(i[0]-iCP[0])
                    ysub=abs(i[1]-iCP[1])
                    sub = xsub if xsub > ysub else ysub
                    sub = int(sub/5)
                    z = int(math.sqrt(xsub**2 + ysub**2))
                    
                    #print(f'sub = {sub: 4d}', end='\r')
                    if ((z > 10 and z < 80)and drow == True): 
                        xsum =  iCP[0] + ( (i[0]-iCP[0]) / sub )
                        ysum =  iCP[1] + ( (i[1]-iCP[1]) / sub )
                        xtemp = xsum - iCP[0]
                        ytemp = ysum - iCP[1]

                        k=0
                        while k < sub:
                            xsumtemp = xsum + (xtemp * k)
                            ysumtemp = ysum + (ytemp * k)
                            ele = Elements()
                            ele.setAll(int(xsumtemp), int(ysumtemp), i[2], color)
                            circlelist.append(ele)
                            k += 1
                            
                    ele = Elements()
                    ele.setAll(i[0],i[1],i[2],color)

                    if drow== False :
                        deleteCircles(circlelist,ele)
                    else:
                        circlelist.append(ele)
                    #print(f'circlelist = {len(circlelist): 4d}', end='\r')
                    iCP=i
            j = 0 
            while j < len(circlelist):
                cv2.circle(img,(circlelist[j].x, circlelist[j].y),int(circlelist[j].r/2),circlelist[j].color,-1) 
                j += 1

        
        # 画像の高さ、幅を取得
        height = img.shape[0]
        width = img.shape[1]

        # フォント指定
        fontType = cv2.FONT_HERSHEY_SIMPLEX
        # テキスト表示
        mode = "oekaki mode" if drow else "keshigomu mode"  
        cv2.putText(img, mode,(int(width)-200,int(height)-20), fontType, 0.7, (0, 0, 0), 2, -1)  

        cv2.imshow('detected 1',img)

        key = cv2.waitKey(10)

        if key is ord('x'):
            circlelist = []
            flag = False

        if key is ord('d'):
            drow = False

        if key is ord('w'):
            drow = True

        if (key is ord('r')
        or key is ord('g')
        or key is ord('b')
        or key is ord('k')):
            color=change_color(key)

        if key is ord('q'):
            picture(img)

        if key is ord('e'):
            break


    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    #pictureフォルダを作成
    make_dir()
    detect_line_segments_demo()
