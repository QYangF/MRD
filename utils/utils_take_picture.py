import cv2
import numpy as np
import time

def take_picture():
    cap = cv2.VideoCapture(1)
    cap.open(1)
    time.sleep(0.3)
    success, img_bgr = cap.read()
    

    cv2.imwrite('D:/myProject/HRI/temp/detect.jpg', img_bgr)
    cv2.imwrite('D:/myProject/HRI/temp/draw.jpg', img_bgr)

    cv2.imshow('camera', img_bgr) 
    cv2.destroyAllWindows() 
