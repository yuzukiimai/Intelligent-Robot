import cv2
import numpy as np


def find_target(image, limit):
    # hsv空間の作成
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    # 取得画像のサイズでhsv空間の配列を作成
    mask = np.zeros(h.shape, dtype=np.uint8)
    # 表示用にmaskと同じサイズの配列を作成
    hsv_scale = np.copy(mask)
    # hsvのしきい値で二値化
    if limit[0] > limit[1]:
        mask[((h > limit[0] * (255/360)) | (h < limit[1] * (255/360)))
             & ((limit[3] < s) & (s < limit[2]))] = 255
    else:
        mask[((h > limit[0] * (255/360)) & (h < limit[1] * (255/360)))
             & ((limit[3] < s) & (s < limit[2]))] = 255
    # 輪郭計算
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []
    # 計算した輪郭をなめらかにマルっと包み込む
    for contour in contours:
        approx = cv2.convexHull(contour)
        area = cv2.contourArea(approx)
        # デカすぎor小さすぎな領域はスキップ
        if area < 1e2 or 1e5 < area:
            continue
        # 最小外接円で近似
        (x, y), radius = cv2.minEnclosingCircle(approx)
        # 返り値準備
        center = (int(x), int(y))
        radius = int(radius)
        circles.append(np.array((center, radius)))
        hsv_scale = mask
    return circles, hsv_scale


# メイン処理
if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    print(type(capture))
    # しきい値
    lim = []
    lim.append([340, 18, 230, 140])  # 赤
    lim.append([40, 60, 290, 210])  # 黄
    lim.append([215, 230, 280, 230])  # 青

    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(width, height)

    while cv2.waitKey(5) != 27:

        _, frame = capture.read()
        image = frame.copy()
        mask = frame.copy()
        detect = []
        for i in range(3):
            circles, scale = find_target(frame, lim[i])
            for target in circles:
                detect.append([target[0], target[1], i])
                so = np.array(detect)
           
        so = so[so[:, 1].argsort()[::-1]]
        for n, ball_data in enumerate(so):
            if ball_data[1] < 30:
                continue
            x, y = ball_data[0]
            cv2.circle(image, ball_data[0], ball_data[1], (0, 0, 0), 2)
            if ball_data[2] == 0:
                cv2.putText(
                    image, 'red', (x-20, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
              
            elif ball_data[2] == 1:
                cv2.putText(
                    image, 'yellow', (x-33, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 217, 255), 2, cv2.LINE_AA)
              
            else:
                cv2.putText(
                    image, 'blue', (x-25, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
        cv2.imshow('color_detect', image)

    capture.release()
    cv2.destroyAllWindows()
