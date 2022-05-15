import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# VideoCaptureのインスタンスを作成する。
# 引数でカメラ選択
cap = cv2.VideoCapture(0)

while True:
    # VideoCaptureから1フレーム読み込む
    ret, frame = cap.read()
    #HSVに変換
    f_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #画像のサイズと検出した色を格納する配列を用意
    height = f_hsv.shape[0]
    width = f_hsv.shape[1]
    pixels = []
    
    #各ピクセルで閾値を満たしたらpixels[]に格納する
    for y in range(height):
        for x in range(width):
            if (f_hsv[y, x, 1] > 45 and 32 < f_hsv[y, x, 2]):
                pixels.append(f_hsv[y, x, 0])
    
    #12分割して色を判断（ヒストグラムの出力）
    plt.xlim(0,180) # x軸の範囲
    plt.xticks(np.arange(0, 180 + 1, 15)) # x軸の目盛りの設定
    plt.hist(pixels, bins=12, range=(0,180)) # ヒストグラムの出力 
    plt.pause(.001)
    
    #最頻値を求めてその画像の色を判断
    # 軸の作成 (0から180を13等分[12個の区間を出したいため]) 
    bins = np.linspace(0, 180, 13)  
    # pixelsをそれぞれの要素を12分割した色範囲に格納  
    index = np.digitize(pixels,bins) 
    # 最頻値
    c = Counter(index)
    print(c)
    mode = c.most_common(1)
    # 最頻値の出力
    print(mode[0][0])
    
    #カメラ映像の出力
    cv2.imshow('Raw Frame', frame)

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
