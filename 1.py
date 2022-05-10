import cv2
import numpy as np
 
cap = cv2.VideoCapture(0) # 任意の動画
 
while True:
    ret, frame = cap.read()
 
    #マスク画像取得
    def getMask(l, u):
        # HSVに変換
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
        lower = np.array(l)
        upper = np.array(u)
        if lower[0] >= 0:
            mask = cv2.inRange(hsv, lower, upper)
        else:
            #赤用（彩度、明度判定は簡略化）
            h = hsv[:, :, 0]
            s = hsv[:, :, 1]
            mask = np.zeros(h.shape, dtype=np.uint8)
            mask[((h < lower[0]*-1) | (h > upper[0])) & (s > lower[1])] = 255
 
        return cv2.bitwise_and(frame,frame, mask= mask)
 
    # 輪郭取得
    def getContours(img,t,r):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)
        imgEdge, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
        # 一番大きい輪郭を抽出
        contours.sort(key=cv2.contourArea, reverse=True)
 
        #一つ以上検出
        if len(contours) > 0:
            cnt = contours[0]
 
 
            # 最小外接円を描く
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
 
            if radius > r:
                return cv2.circle(frame,center,radius,(0,255,0),2)
            else:
                return frame
        else:
            return frame
    # 青・緑・赤マスク
    res_blue = getMask([110,45,30], [150,255,255])
    res_green = getMask([20,35,30], [50,255,255])
    res_red = getMask([-10,10,30], [150,255,255])
 
    #輪郭取得
    getContours(res_blue, 30, 75) # (画像, 明度閾値, 最小半径)
    contours_frame = getContours(res_green, 30, 75)
    contours_frame = getContours(res_red, 30, 75)
 
 
    # 再生する場合
    #cv2.imshow('video', contours_frame)
    cv2.imshow('image', frame)
    key = cv2.waitKey(1)
    if key != -1:
        break
    
cap.release()
cv2.destroyAllWindows()
