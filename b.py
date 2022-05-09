import cv2
import numpy as np

v = cv2.VideoCapture(0)
while(v.isOpened()):
    r, f = v.read()
    if ( r == False ):
        break
    mono = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    r, dst = cv2.threshold(mono, 0, 255, cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(f, contours, -1, (0, 255, 0), 3)
    cv2.imshow("", f)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

v.release()
cv2.destroyAllWindows()
