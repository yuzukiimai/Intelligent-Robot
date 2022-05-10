import cv2
import numpy as np
 
cap = cv2.VideoCapture(0) # 任意の動画
while(1):
    _, frame = cap.read()
    # HSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # 白のHSV範囲
    lower_white = np.array([0,0,100])
    upper_white = np.array([180,45,255])
 
    # 白以外にマスク
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    res_white = cv2.bitwise_and(frame,frame, mask= mask_white)
 
    # 輪郭抽出
    gray = cv2.cvtColor(res_white, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
    imgEdge, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    # 一番大きい輪郭を抽出
    contours.sort(key=cv2.contourArea, reverse=True)
    cnt = contours[0]
 
    # 最小外接円を描く
    (x,y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    img = cv2.circle(frame,center,radius,(0,255,0),2)
 
    # 再生
    cv2.imshow('video',img)
    k = cv2.waitKey(25) & 0xFF
 
    #Q で終了
    if k == ord('q'):
        break
 
cv2.destroyAllWindows()
