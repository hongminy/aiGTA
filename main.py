import     numpy         as      np
from       PIL           import  ImageGrab
import     cv2
import     time
from Driver              import  Driver
import     win32gui, win32ui, win32con, win32api
from       Debuger       import  Debuger
from       screenGrabber import  Screen
from       numpy         import  ones,vstack
from       numpy.linalg  import  lstsq
from       statistics    import  mean
import     pyautogui

if __name__ == "__main__":
    s = Screen()
    s.get_screen()
