import     numpy         as      np
from       PIL           import  ImageGrab
import     cv2
import     time
from       Driver        import  Driver
import     win32gui, win32ui, win32con, win32api
from       Debuger       import  Debuger
from       numpy         import  ones,vstack
from       numpy.linalg  import  lstsq
from       statistics    import  mean
from       getkeys       import  key_check
import     os

debug = True
if debug: debuger = Debuger()


def keys_to_output(keys):
    # convert pressed keys to an array
    #[A,W,D]
    output = [0,0,0]
    
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1

    return output

file_name = 'training_data.npy'
if os.path.isfile(file_name):
    debuger.deb("training file exist, loading previous data")
    training_data = list(np.load(file_name))
else:
    debuger.deb("training file not exist, start fresh")
    training_data = []
    




class Screen:
    def get_region_of_interest(self, img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        # filled that mask by the vertices
        masked = cv2.bitwise_and(img, mask)
        return masked
        


    def waitsecs(self, sec = 5):
        # print 5, 4, 3, 2, 1 for users to ready
        for i in list(range(1, sec + 1))[::-1]:
            print(i ,'..')
            time.sleep(1)
        print("READY!GO")

    def draw_lines(self, img, lines):
        # take image and lines
        # draw lines on that image
        try:
            for line in lines:
                coords = line[0]
                cv2.line(img, (coords[0],coords[1]),
                              (coords[2],coords[3]),
                              [255,255,255], 3)
        except:
            pass

    def draw_lanes(self, img, lines, color=[0, 255, 255], thickness=3):

        # if this fails, go with some default line
        try:

            # finds the maximum y value for a lane marker 
            # (since we cannot assume the horizon will always be at the same point.)

            ys = []  
            for i in lines:
                for ii in i:
                    ys += [ii[1],ii[3]]
            min_y = min(ys)
            max_y = 600
            new_lines = []
            line_dict = {}

            for idx,i in enumerate(lines):
                for xyxy in i:
                    # These four lines:
                    # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                    # Used to calculate the definition of a line, given two sets of coords.
                    x_coords = (xyxy[0],xyxy[2])
                    y_coords = (xyxy[1],xyxy[3])
                    A = vstack([x_coords,ones(len(x_coords))]).T
                    m, b = lstsq(A, y_coords)[0]

                    # Calculating our new, and improved, xs
                    x1 = (min_y-b) / m
                    x2 = (max_y-b) / m

                    line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                    new_lines.append([int(x1), min_y, int(x2), max_y])

            final_lanes = {}

            for idx in line_dict:
                final_lanes_copy = final_lanes.copy()
                m = line_dict[idx][0]
                b = line_dict[idx][1]
                line = line_dict[idx][2]
                
                if len(final_lanes) == 0:
                    final_lanes[m] = [ [m,b,line] ]
                    
                else:
                    found_copy = False

                    for other_ms in final_lanes_copy:

                        if not found_copy:
                            if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                                if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                                    final_lanes[other_ms].append([m,b,line])
                                    found_copy = True
                                    break
                            else:
                                final_lanes[m] = [ [m,b,line] ]

            line_counter = {}

            for lanes in final_lanes:
                line_counter[lanes] = len(final_lanes[lanes])

            top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

            lane1_id = top_lanes[0][0]
            lane2_id = top_lanes[1][0]

            def average_lane(lane_data):
                x1s = []
                y1s = []
                x2s = []
                y2s = []
                for data in lane_data:
                    x1s.append(data[2][0])
                    y1s.append(data[2][1])
                    x2s.append(data[2][2])
                    y2s.append(data[2][3])
                return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

            l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
            l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

            return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
        except Exception as e:
            print(str(e))


    def process_image(self, img):
        originalImage = img
        #convert the given image to grey
        processedImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        # edge detection
        processedImage = cv2.Canny(processedImage,
                                   threshold1 = 200,
                                   threshold2 = 300)
        
        processedImage = cv2.GaussianBlur(processedImage, (5,5), 0)
        # gaussian blur the image to get rid of the jelly 
        vertices = np.array([[10,500], [10,300], [300,200],
                            [500,200], [800,300], [800,500]], np.int32)
        # this array is tweackable, and this one is good for scooter
        # different vehicles need differents param here
        # cutting out the area of instrument panel (1st person view)or 
        # the aera of vehicle itself (if it is in 3rd person view)
          
        processedImage = self.get_region_of_interest(processedImage, [vertices])

        lines = cv2.HoughLinesP(processedImage, 1, np.pi/180, 180, 20, 15)
        #                      edges, 1, np.array is xuanxue, minlinelength, maxlinegap
        # tweakable too
        # The HoughLine Transform Algorithm

        m1 = 0
        m2 = 0
        try:
            l1, l2, m1, m2 = self.draw_lanes(originalImage, lines)
            cv2.line(originalImage, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
            cv2.line(originalImage, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
        except Exception as e:
            print(str(e))
            pass

        try:
            for coords in lines:
                coords = coords[0]
                try:
                    cv2.line(processedImage, (coords[0], coords[1]),
                             (coords[2], coords[3]), [255,0,0], 3)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            pass
        
        #self.draw_lanes(processedImage, lines)
        return processedImage, originalImage, m1, m2

    def grab_screen(self, region=None):

        hwin = win32gui.GetDesktopWindow()

        if region:
                left,top,x2,y2 = region
                width = x2 - left + 1
                height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)


        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
        
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        

    def get_screen(self):
        self.waitsecs(5)
        lastTime = time.time()
        while(True):
            if debug: debuger.deb(("Loop takes {} secs".format(time.time() - lastTime)))
            lastTime = time.time()

            frame = self.grab_screen(region=(0,40,800,640))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame,(80,60))
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([frame, output])
            if len(training_data) %500 ==0:
                debuger.deb("have {} training data(s)".format(len(training_data)))
                np.save(file_name, training_data)
                
            

           
if __name__ == "__main__":
    s = Screen()
    s.get_screen()
