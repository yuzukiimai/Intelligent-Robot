import numpy as np
import cv2

cap = cv2.VideoCapture(0) #カメラを定義

def red_range(img): #赤色の領域をマスクする関数
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #BGRをHSV色空間に変換

#赤色の領域を閾値でフィルタリング
#OpenCVのHSV色空間では赤は0~30付近と150~180付近に分かれるが、
#181~255は0からの循環なので180を中心に範囲を取れば赤の閾値を一回で指定できる。たぶん。
    hsv_min = np.array([170,170,60]) #色相(Hue)、彩度(Saturation)、明度(Value)
    hsv_max = np.array([190,255,255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max) #hsvの各ドットについてhsv_minからhsv_maxの範囲内ならtrue

    return mask

while( cap.isOpened() ): #カメラが使える限りループ

    ret, frame = cap.read() #カメラの情報を取得。frameに640x480x3の配列データが入る。
    frame_np = red_range(np.array(frame)) #frameデータをnp配列に変換。

#領域のカタマリである「ブロブ」を識別し、データを格納する。すごくありがたい機能。
    nLabels, labelimages, data, center = cv2.connectedComponentsWithStats(frame_np)

    blob_count = nLabels - 1 #ブロブの数。画面領域全体を1つのブロブとしてカウントするので、-1する。

    if blob_count >= 1: #ブロブが1つ以上存在すれば、画面全体を示すブロブデータを削除。
        data = np.delete(data, 0, 0)
        center = np.delete(center, 0, 0)

#認識したブロブの中で最大領域を持つもののインデックスを取得
    tbi = np.argmax(data[:, 4]) #target_blob_index

#最大ブロブの中心に青の円マークを直径10pix、太さ3pixで描く
    cv2.circle(frame,(int(center[tbi][0]),int(center[tbi][1])),10,(255,0,0),3)

#画像を表示する
    cv2.imshow('RaspiCam_Live',frame)

#キーが押されたら終了する
    if cv2.waitKey(1) != -1:
        break

#終了処理。カメラを解放し、表示ウィンドウを破棄。
cap.release()
cv2.destroyAllWindows()
