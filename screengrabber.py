import numpy as np
from PIL import ImageGrab
import cv2
import time
from directKey import PressKey, ReleaseKey, W, A, S, D
from Debuger import Debuger

debug = False



def waitsecs(sec = 5):
    # print 5, 4, 3, 2, 1 for users to ready
    for i in list(range(1, sec + 1))[::-1]:
        print(i ,'..')
        time.sleep(1)
    print("READY!GO")

def process_image(originalImage):
    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.Canny(processedImage,
                               threshold1 = 200,
                               threshold2 = 300)
    return processedImage

def get_screen():
    waitsecs()
    if debug: debuger = Debuger("Debug info for getscreen(): ")
    lastTime = time.time()
    while(True):
        if debug: debuger.deb(("Loop takes {} secs".format(time.time() - lastTime)))
        lastTime = time.time()
        #frame = np.array(ImageGrab.grab(bbox=(130,64,880,624)))
        frame = np.array(ImageGrab.grab(bbox=(0,40,800,636)))
        edgeDetection = process_image(frame)
        #cv2.imshow('GameCapture', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cv2.imshow('edge_detection', edgeDetection)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

get_screen()
