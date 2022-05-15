import cv2
import numpy as np
 
cap = cv2.VideoCapture('ball.mp4') # 任意の動画
 
while(1):
    _, frame = cap.read()
    frameOrig = frame
    #ボール１つのサイズ
    ballSize = 9200
    # 射影変換
    rows, cols, ch = frame.shape
    pts1 = np.float32([[0, 0], [1280, 0], [0, 720], [1280, 720]])
    pts2 = np.float32([[0, 0], [1280, 0], [0, 720], [1280, 720]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(frame, M, (1280, 720))
    frame = dst
 
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
 
        #ボールの面積計算
        ballPixels = cv2.countNonZero(mask)
        ballNum = str(round(ballPixels / ballSize))
 
        return cv2.putText(frameOrig, ballNum, (100, 650), cv2.FONT_HERSHEY_SIMPLEX, 8.0, (255, 255, 255), thickness=10)
 
    # 黄色マスク
    num_frame = getMask([30,100,100], [40,255,255])
 
    # 再生
    cv2.imshow('video',num_frame)
 
    k = cv2.waitKey(25) & 0xFF
    #Q で終了
    if k == ord('q'):
        break
 
 
cv2.destroyAllWindows()
