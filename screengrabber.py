import numpy as np
from PIL import ImageGrab
import cv2

def get_screen():
    while(True):
        #frame = np.array(ImageGrab.grab(bbox=(130,64,880,624)))
        frame = np.array(ImageGrab.grab(bbox=(0,40,800,636)))
        cv2.imshow('GameCapture', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

get_screen()