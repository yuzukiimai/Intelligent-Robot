import cv2
import time
from matplotlib import pyplot as plt

# USBカメラのID番号
no = 0

# USBカメラから映像を取り込む
cap_0 = cv2.VideoCapture(no)

cap_0.set(3, 1920)
cap_0.set(4, 1080)
cap_0.set(5, 30)

if cap_0.isOpened() is False:
    raise("IO Error")

colors = ("r", "g", "b")

while True:
    # 時間測定開始
    t1 = time.time()

    is_ok_0, img_0 = cap_0.read()

    print(cap_0.get(3), cap_0.get(4), cap_0.get(5))
    #print(is_ok_0)

    if is_ok_0 == False:
        continue

    # 画像の切り抜き（取り込み画像を1：1にする, Y:X）
    img_a = img_0[90:990, 510:1410]

    # プロットの初期化
    plt.clf()

    # RGBごとにヒストグラムを計算しプロット
    for i, channel in enumerate(colors):
        histgram = cv2.calcHist([img_a], [i], None, [256], [0, 256])
        plt.plot(histgram, color = channel)
        plt.xlim([0, 256])

    # プロットの更新間隔。カッコの中は時間(msec)
    plt.pause(0.001)

    # 時間計測終了
    elapsedTime = time.time() - t1

    # フレームレートの計算
    fps = "{:.0f}FPS".format(1/elapsedTime)

    # 画面にfpsを表示させる
   # cv2.putText(img_a, fps, (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2, cv2.LINE_AA)
    
    # USBカメラから取り込んだ映像を表示
    cv2.imshow('cap_test_a', img_a)

    # 画面表示位置の指定(表示画面の名前, x座標, y座標)
   # cv2.moveWindow('cap_test_a', 200, 50)  

    # グラフの表示位置を指定
   # fig_place = plt.get_current_fig_manager()

    # カッコの中(windows画面のx座標，y座標，表示させる図の幅，図の高さ)
   # fig_place.window.setGeometry(1112, 85, 640, 480)  

    k = cv2.waitKey(10)
    
    if k == ord('q'):
        break

cap_0.release()
cv2.destroyAllWindows()
