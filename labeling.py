#-*- coding: utf-8 -*-


import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()

    #hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([150, 255, 255])
    img_mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    img_color_blue = cv2.bitwise_and(img, img, mask=img_mask_blue
                                     
                                     
    #labeling
    label_blue = cv2.connectedComponentsWithStats(gray)
    n_blue = label_blue[0] - 1
    data_blue = np.delete(label_blue[2], 0, 0)
    center_blue = np.delete(label_blue[3], 0, 0)

                                     
    #word
    font_size = 3
    font = cv2.FONT_HERSHEY_PLAIN

    for k in range(n_blue):
        img = cv2.circle(img,(int(center_blue[k][0]),int(center_blue[k][1])), 10, (255,0,0), -1)
        cv2.putText(img,"blue", (int(center_blue[k][0]) - 30, int(center_blue[k][1]) - 10),font, font_size,(255,0,0))
        cv2.imshow("ball", img)

    #ラベルの個数nだけ色を用意
    #print u"ブロブの個数:", n
    #print u"各ブロブの外接矩形の左上x座標", data[:,0]
    #print u"各ブロブの外接矩形の左上y座標", data[:,1]
    #print u"各ブロブの外接矩形の幅", data[:,2]
    #print u"各ブロブの外接矩形の高さ", data[:,3]
    #print u"各ブロブの面積", data[:,4]
    #print u"各ブロブの中心座標:\n",center

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
