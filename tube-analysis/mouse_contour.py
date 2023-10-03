import numpy as np
import cv2 
import matplotlib.pyplot as plt

class DrawRectangle:
   
    def __init__(self, img=None):
        """Takes in one frame"""

        # set image, if none create blank black image
        if img is None:
            img = np.zeros((512,512,3))
        self.img = img

        # rectangle coords init
        self.start_coords = {"x":None, "y":None}
        self.stop_coords = {"x":None, "y":None}
        self.area = None

    def on_mouse(self, event, x, y, flags, params):

        if event == cv2.EVENT_LBUTTONDOWN:
            # print(f"Start Mouse Position: {x}, {y}")
            self.start_coords["x"] = x
            self.start_coords["y"] = y

        elif self.start_coords["x"] is not None and event == cv2.EVENT_MOUSEMOVE:
            self.temp_rectangle(x, y)
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            # print(f"End Mouse Position: {x}, {y}")
            self.stop_coords["x"] = x
            self.stop_coords["y"] = y
            self.rectangle_area()
            
        # elif event == cv2.EVENT_RBUTTONUP:
        #     self.rectangle_area()
        #     return

    def temp_rectangle(self, x, y):
        pt1 = (self.start_coords["x"], self.start_coords["y"])
        cv2.rectangle(self.img, pt1=pt1, pt2=(x, y), color=(255,0,255), thickness=1)
    
    def draw_rectangle(self):
        pt1 = (self.start_coords["x"], self.start_coords["y"])
        pt2 = (self.stop_coords["x"], self.stop_coords["y"])

        if self.ready_to_draw():
            cv2.rectangle(self.img, pt1=pt1, pt2=pt2, color=(255,0,255), thickness=1)

    def show_img(self):
        cv2.imshow("image", self.img)

    def ready_to_draw(self):
        if self.stop_coords["x"] is not None and self.stop_coords["y"] is not None:
            return True
        else:
            return False
        
    def rectangle_area(self):
        x0 = self.start_coords["x"]
        x1 = self.stop_coords["x"]
        y0 = self.start_coords["y"]
        y1 = self.stop_coords["y"]

        length = x1 - x0
        height = y1 - y0
        area_px = length*height

        self.area = np.abs(area_px)
        # print(f"Rectangle area: {area_px} pix")

        # return

if __name__ == "__main__":

    def do_frame(img):
        draw_rect = DrawRectangle(img)
        while draw_rect.area is None:
            cv2.namedWindow('real image')
            cv2.imshow('real image', img)
            cv2.setMouseCallback('real image', draw_rect.on_mouse, 0)

            draw_rect.draw_rectangle()
            # area = draw_rect.area
            # print(draw_rect.start_coords, draw_rect.stop_coords, area)
                
            if cv2.waitKey(10) & 0xFF == 27:
                cv2.destroyAllWindows()
                break
            
        return draw_rect.area

    img = cv2.imread("C:\\Users\\alicl\\Documents\\GitHub\\salp-research\\tube-analysis\\media\\shell_screenshot.png")
    vid_path = "C:\\Users\\alicl\\Documents\\GitHub\\salp-research\\tube-analysis\\media\\shell_10-3.mp4" 

    # area_list = []
    # t = []

    # cap = cv2.VideoCapture(vid_path)
    # count = 0
    # fps = 30

    # while (cap.isOpened()):
    #     ret, frame = cap.read()
    #     # do processing if video still has frames left
    #     if ret:
    #         # grab a frame every second (residual is zero)
    #         if count%fps==0:
    #             # cv2.imshow("raw", frame)
    #             area = do_frame(frame)
    #             print(area)
    #             area_list.append(area)
    #             timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
    #             t.append(timestamp / 1000.0)
    #         count += 1

    #         # cleanup if manually ended ("q" key pressed)
    #         if cv2.waitKey(25) & 0xFF == ord('q'):
    #             cap.release()
    #             cv2.destroyAllWindows()
       
    #     # cleanup if video ends
    #     else:
    #         cap.release()
    #         cv2.destroyAllWindows()

    # np.save("area_pix_10-3.npy", np.array(area_list))
    # np.save("t.npy", np.array(t))

    area = np.load("area_pix_10-3.npy", allow_pickle=True)
    t = np.load("t.npy", allow_pickle=True)

    fig, ax = plt.subplots(1,1)
    ax.plot(t, area)
    plt.show()



    

   