import numpy as np
from PIL import ImageGrab
import cv2

def process_image(originalImage):
    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.Canny(processedImage,
                               threshold1 = 200,
                               threshold2 = 300)
    return processedImage

def get_screen():
    while(True):
        #frame = np.array(ImageGrab.grab(bbox=(130,64,880,624)))
        frame = np.array(ImageGrab.grab(bbox=(0,40,800,636)))
        edgeDetection = process_image(frame)
        #cv2.imshow('GameCapture', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cv2.imshow('edge_detection', edgeDetection)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

get_screen()
