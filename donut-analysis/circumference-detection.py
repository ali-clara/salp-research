import numpy as np
import cv2
import matplotlib.pyplot as plt

## calibrate with a contour of known size and the procedure here: 
# https://pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/


# HSV mask values

# 1
blue_min = np.array([55, 30, 40],np.uint8)
blue_max = np.array([170, 255, 165],np.uint8)

# 3b
# blue_min = np.array([55, 30, 40],np.uint8)
# blue_max = np.array([170, 255, 155],np.uint8)

## ----------------- Image Pre-Processing ----------------- ##

def crop_image(img):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]

    w_margin = int(width/3.5)
    h_margin = int(height/3)

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
        blurred = cv2.blur(image, (10, 10))
        hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        masked_img = cv2.inRange(hsv_img, blue_min, blue_max)
    elif color == "black":
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.blur(grey, (10, 10))
        masked_img = blurred
    
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

def find_circumference(radius):
    return np.pi*2*radius

## ----------------- Contour Detection ----------------- ##

def detect_edges(image, display=False):
    edge_detected_image = cv2.Canny(image, 
                                    threshold1=30, 
                                    threshold2=130)
    
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
    c = find_circumference(r)    # circumference of donut (mm)

    # many magic numbers, am working on generalizing
    contour_list = []
    for i, contour in enumerate(contours):
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if ((len(approx) > 8) & (area > 10000) & (perimeter > 400) & (perimeter < 800)):
        # if ((len(approx) > 8) & 
        #     (area > area_of_circle(mm_to_pixel(r, pix_per_mm=cal_value))) & 
        #     (perimeter > mm_to_pixel((c-70), pix_per_mm=cal_value)) & 
        #     (perimeter < mm_to_pixel((c+70), pix_per_mm=cal_value))):

            # print(f"appending contour {i} to list")
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
            cv2.imshow("mask", masked_frame)
            edges = detect_edges(masked_frame)
            cv2.imshow("edges", edges)

            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            square_merged = merge_contours(contours)
            perim = cv2.arcLength(square_merged, True)
            calibration_perimeter.append(perim)

            # to connect the dots, do [contour] instead of contour
            cv2.drawContours(frame, [square_merged], -1, (255,0,0), 2)
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
    area_list = []
    t = []

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
            
            # cv2.drawContours(frame, contour_list_raw, 2, (0,255,0), 2)
            # cv2.imshow("raw contours", frame)

            # if we can grab a contour, record the area and circumference. Otherwise record NAN
            if len(contour_list_filtered) != 0:
                merged_contours = merge_contours(contour_list_filtered)
                perimeter = cv2.arcLength(merged_contours, False)
                area = cv2.contourArea(merged_contours)
                perimeter = pixel_to_mm(perimeter, cal_value)
                sqrt_area = pixel_to_mm(np.sqrt(area), cal_value)
                
                circumference.append(perimeter)
                area_list.append(sqrt_area**2)
        
                cv2.drawContours(frame, [merged_contours], -1, (0,255,0), 2)
            else:
                area_list.append(np.nan)
                circumference.append(np.nan)
            
            # grab timestamp
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            t.append(timestamp / 1000.0)
            print(timestamp/1000)
            
            cv2.imshow('Objects Detected', frame)

            # cleanup if manually ended ("q" key pressed)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return circumference, area_list, t
        
        # cleanup if video ends
        else:
            cap.release()
            cv2.destroyAllWindows()
            return circumference, area_list, t

##  ----------------- Flight Code ----------------- ##

if __name__ == "__main__":
    img_path = "media/donut-screenshot.png"
    vid_1 = "media/donut-video.mp4"
    vid_2 = "media/donut-5W.mp4"
    # cal_path = "media/8-1-23/calibration.mp4"

    def calibrate(cal_path):
        calibration_perim = calibration(cal_path)
        average_perim = np.mean(calibration_perim)
        true_perim = 81.33 # mm, measured perimeter of square

        pix_per_mm = average_perim / true_perim

        print(f"The average calibration square perimeter was {average_perim} px")
        print(f"Calibration value: {pix_per_mm} pix/mm")

        return pix_per_mm
    
    def do_video(vid_path, pix_per_mm, file_date, file_name, donut_color="blue"):
        circumference_list, area_list, t = video_capture(vid_path, pix_per_mm, donut_color)
        try: 
            np.save('data/'+file_date+'/circ_'+file_name+'.npy', np.array(circumference_list))
            np.save('data/'+file_date+'/area_'+file_name+'.npy', np.array(area_list))
            np.save('data/'+file_date+'/t_'+file_name+'.npy', np.array(t))
        except FileNotFoundError:
            print("Folder not found, check your working directory or your spelling. Saving to parent directory instead")
            np.save('circ_'+file_name+'.npy', np.array(circumference_list))
            np.save('area_'+file_name+'.npy', np.array(area_list))
            np.save('t_'+file_name+'.npy', np.array(t))
 
    def do_photo():
        raw_image = read_and_crop(img_path, display=True)
        # mask = mask_image(raw_image)
        # edge_image = detect_edges(mask)
        # contour_list = detect_contours(raw_image, edge_image)
        # perimeter = cv2.arcLength(contour_list[0], True)
    
    # calibration_value = calibrate("media/8-31-23/calibration-1.mp4") # number of pixels per mm of image

    # do_video(vid_2, 7.31)
    # do_video("media/8-16-23/5W.mp4", pix_per_mm=8.06, file_date="8-16-23", file_name="5W")

    
    # names = ["1a", "1b", "2a", "2b", "3a", "3b"]
    names = ["2a"]
    for name in names:
        do_video("media/8-31-23/donut-"+name+".mp4", pix_per_mm=8.57, file_date="8-31-23", file_name=name)


    # a1 = np.load("data/8-31-23/area_1a.npy")
    # t1 = np.load("data/8-31-23/t_1a.npy")
    # a1b = np.load("data/8-31-23/area_1b.npy")
    # t1b = np.load("data/8-31-23/t_1b.npy")
    # a2 = np.load("data/8-31-23/area_2a.npy")
    # t2 = np.load("data/8-31-23/t_2a.npy")

    # print(len(a2))
    # print(t2[3500])

    # print(len(a1))
    # print(t1[3500])

    # fig, ax = plt.subplots(1,1)
    # ax.plot(t1, a1)
    # ax.plot(t1b, a1b)
    # ax.plot(t2, a2)
    # plt.show()

