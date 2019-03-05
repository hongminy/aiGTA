import     numpy     as      np
from       PIL       import  ImageGrab
import     cv2
import     time
from       directKey import  PressKey, ReleaseKey, W, A, S, D
from       Debuger   import Debuger
import     pyautogui

debug = False

def get_region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    # filled that mask by the vertices
    masked = cv2.bitwise_and(img, mask)
    return masked
    


def waitsecs(sec = 5):
    # print 5, 4, 3, 2, 1 for users to ready
    for i in list(range(1, sec + 1))[::-1]:
        print(i ,'..')
        time.sleep(1)
    print("READY!GO")

def process_image(originalImage):
    # convert the given image to grey
    processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    processedImage = cv2.Canny(processedImage,
                               threshold1 = 200,
                               threshold2 = 300)
    
    vertices = np.array([[10,500], [10,300], [300,200],
                        [500,200], [800,300], [800,500]])
    # this array is twickable, and this one is good for scooter
    # different vehicles need differents param here
    # cutting out the area of instrument panel (1st person view)or 
    # the aera of vehicle itself (if it is in 3rd person view)
    
    processedImage = get_region_of_interest(processedImage, [vertices])
    return processedImage

def get_screen():
    waitsecs()
    if debug: debuger = Debuger("Debug info for getscreen(): ")
    lastTime = time.time()
    while(True):
        if debug: debuger.deb(("Loop takes {} secs".format(time.time() - lastTime)))
        lastTime = time.time()
        frame = np.array(ImageGrab.grab(bbox=(0,40,800,636)))
        edgeDetection = process_image(frame)
        cv2.imshow('edge_detection', edgeDetection)
        # display the opencv detected edges

        # press q to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

get_screen()
