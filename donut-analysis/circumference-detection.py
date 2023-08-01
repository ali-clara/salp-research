import numpy as np
import cv2
import matplotlib.pyplot as plt

## calibrate with a contour of known size and the procedure here: 
# https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/


# HSV mask values
blue_min = np.array([80, 60, 51],np.uint8)
blue_max = np.array([110, 255, 170],np.uint8)

## ----------------- Image Pre-Processing ----------------- ##

def crop_image(img):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]

    w_margin = int(width/4)
    h_margin = int(height/3.5)

    # crop: img[y:y+h, x:x+w]
    img = img[h_margin:(height-h_margin), w_margin:(width-w_margin)]

    return img

def read_and_crop(path, display=False):
    img = cv2.imread(path)
    img = crop_image(img)

    if display == True:
        cv2.imshow("raw image", img)
        cv2.waitKey(0)

    return img

def mask_image(image, color, display=False):
    
    if color != "black":
        blurred = cv2.blur(image, (9, 9))
        hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        masked_img = cv2.inRange(hsv_img, blue_min, blue_max)
    elif color == "black":
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        masked_img = cv2.blur(grey, (3, 3))
    
    if display == True:
        cv2.imshow('hsv mask', masked_img)
        cv2.waitKey(0)

    return masked_img

##  ----------------- Size Calibration Helpers ----------------- ##

def pixel_to_mm(pixel, pix_per_mm):
    return pixel / pix_per_mm

def mm_to_pixel(mm, pix_per_mm):
    return mm * pix_per_mm

def area_of_circle(radius):
    return np.pi*radius**2

def circumference(radius):
    return np.pi*2*radius

## ----------------- Contour Detection ----------------- ##

def detect_edges(image, display=False):
    edge_detected_image = cv2.Canny(image, 
                                    threshold1=100, 
                                    threshold2=200)
    
    if display == True:
        cv2.imshow('canny edge detection', edge_detected_image)
        cv2.waitKey(0)

    return edge_detected_image

def detect_contours(raw_image, edge_image, cal_value, display=False):
    """
    Detects and filters contours to select for the donut inner circle 
        https://www.authentise.com/post/detecting-circular-shapes-using-contours"""

    contours, hierarchy = cv2.findContours(edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    r = 14  # approximate radius of donut (mm)
    c = circumference(r)    # circumference of donut (mm)

    # many magic numbers, am working on generalizing
    contour_list = []
    for i, contour in enumerate(contours):
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if ((len(approx) > 8) & (area > 13000) & (perimeter > 500) & (perimeter < 800)):
        # if ((len(approx) > 8) & 
        #     (area > area_of_circle(mm_to_pixel(r, pix_per_mm=cal_value))) & 
        #     (perimeter > mm_to_pixel((c-70), pix_per_mm=cal_value)) & 
        #     (perimeter < mm_to_pixel((c+70), pix_per_mm=cal_value))):

            print(f"appending contour {i} to list")
            contour_list.append(contour)

    if display == True:
        cv2.drawContours(raw_image, contour_list, 0, (255,0,0), 2)
        cv2.imshow('Objects Detected', raw_image)
        cv2.waitKey(0)

    return contours, contour_list

def merge_contours(contour_list):
    """
    Takes a list of many contours and merges them into one list
        https://stackoverflow.com/questions/44501723/how-to-merge-contours-in-opencv"""
    
    list_of_pts = [] 
    for contour in contour_list:
        list_of_pts += [pt for pt in contour]

    formatted_pts = np.array(list_of_pts).reshape((-1,1,2)).astype(np.int32)
    merged_contour = cv2.convexHull(formatted_pts)
    return merged_contour

##  ----------------- Calibration   ----------------- ##

def calibration(cal_path):
    cap = cv2.VideoCapture(cal_path)
    calibration_perimeter = []
    # Loop until the end of the video
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # do some preprocessing
            frame = crop_image(frame)
            masked_frame = mask_image(frame, color="black")
            edges = detect_edges(masked_frame)
            cv2.imshow("edges", edges)

            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            inner_square = contours[2]
            inner_square_merged = merge_contours(inner_square)
            perim = cv2.arcLength(inner_square_merged, True)
            calibration_perimeter.append(perim)
            # print(perim)

            # to connect the dots, do [contour] instead of contour
            cv2.drawContours(frame, inner_square_merged, -1, (255,0,0), 2)
            cv2.imshow("contours", frame)

            # cleanup if manually ended ("q" key pressed)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return calibration_perimeter
        
        # cleanup if video ends
        else:
            cap.release()
            cv2.destroyAllWindows()
            return calibration_perimeter

##  ----------------- Video Processing  ----------------- ##
def video_capture(path_to_video, cal_value, color):
    cap = cv2.VideoCapture(path_to_video)
    circumference = []
 
    # Loop until the end of the video
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # do some preprocessing
            frame = crop_image(frame)
            masked_frame = mask_image(frame, color)
            edges = detect_edges(masked_frame)
            # cv2.imshow("raw", frame)
            cv2.imshow("mask", masked_frame)
            cv2.imshow("edges", edges)

            # find image contours
            contour_list_raw, contour_list_filtered = detect_contours(raw_image=frame, edge_image=edges, cal_value=cal_value)
            
            # cv2.drawContours(frame, contour_list_raw, 6, (0,255,0), 2)
            # cv2.imshow("raw contours", frame)

            if len(contour_list_filtered) != 0:
                merged_contours = merge_contours(contour_list_filtered)
                perimeter = cv2.arcLength(merged_contours, False)
                perimeter = pixel_to_mm(perimeter, cal_value)
                circumference.append(perimeter)

                cv2.drawContours(frame, merged_contours, -1, (0,0,255), 2)
           
            cv2.imshow('Objects Detected', frame)

            # cleanup if manually ended ("q" key pressed)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return circumference
        
        # cleanup if video ends
        else:
            cap.release()
            cv2.destroyAllWindows()
            return circumference

##  ----------------- Flight Code ----------------- ##

if __name__ == "__main__":
    img_path = "donut-screenshot.png"
    vid_1 = "donut-video.mp4"
    vid_2 = "donut-5W.mp4"
    cal_path = "8-1-23/calibration.mp4"

    def calibrate():
        calibration_perim = calibration(cal_path)
        print(f"average: {np.mean(calibration_perim)}")

        true_perim = 80 # mm

        pix_per_mm = calibration_perim / true_perim
    
    def do_video(vid_path, pix_per_mm, donut_color="blue"):
        circumference_list = video_capture(vid_path, pix_per_mm, donut_color)
        np.save('circumference-5W.npy', np.array(circumference_list))
 
    def do_photo():
        raw_image = read_and_crop(img_path, display=True)
        # mask = mask_image(raw_image)
        # edge_image = detect_edges(mask)
        # contour_list = detect_contours(raw_image, edge_image)
        # perimeter = cv2.arcLength(contour_list[0], True)
    
    # do_video(vid_2, 7.31)
    # do_video(5.3)

    circumference = np.load("circumference-5W.npy")

    x = np.linspace(0, 87, len(circumference))

    fig, ax = plt.subplots(1,1)
    ax.plot(x, circumference, '.')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Circumference (mm)")
    plt.show()