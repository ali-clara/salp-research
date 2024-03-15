import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob

## ----------------- Helper Functions ----------------- ##

def crop_image(img, crop_type="upper_half"):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]

    # crop: img[y:y+h, x:x+w]
    if crop_type == "lower_half":
        img = img[int(height/2):height, 0:width]
        y_offset = int(height/2)
    else:
        img = img[0:int(height/2), 0:width]
        y_offset = 0
    return img,  y_offset

def resize_image(img, scale_factor=0.75):
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]

    # crop just a little, as a treat
    crop_val = 10
    img = img[int(height/crop_val):int(height-height/crop_val), int(width/crop_val):int(width-width/crop_val)]

    # resize (make 75% of the original size, preserving the ratio)
    img = cv2.resize(img, (int(width*scale_factor), int(height*scale_factor)))

    return img

def mask_image(image, hsv_range):
    """Function that masks the input image given an hsv range"""
    blurred = cv2.blur(image, (2, 2))
    hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    masked_img = cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
    blurred2 = cv2.blur(masked_img, (10, 10))
    _, thresholded_img = cv2.threshold(blurred2, 150, 255, cv2.THRESH_BINARY)

    return thresholded_img
    
def merge_contours(contour_list, y_offset=0):
    """
    Takes a list of many contours and merges them into one list
        https://stackoverflow.com/questions/44501723/how-to-merge-contours-in-opencv"""
    
    list_of_pts = [] 
    for contour in contour_list:
        list_of_pts += [pt+[0, y_offset] for pt in contour]

    formatted_pts = np.array(list_of_pts).reshape((-1,1,2)).astype(np.int32)
    merged_contour = cv2.convexHull(formatted_pts)
    return np.array(merged_contour)

def find_contours_rectangle(raw_image, hsv_range, image_section):
    # crop, mask, and detect the contours of the image
    cropped, y_offset = crop_image(raw_image, crop_type=image_section)
    mask = mask_image(cropped, hsv_range)
    edges = detect_edges(mask)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    merged_contours = merge_contours(contours, y_offset)

    return merged_contours

def find_rectangle_center(leftmost, rightmost, topmost, bottommost):
    """Finds the center of a rectangle based on the four extreme points"""
    true_center = (leftmost[0]+(rightmost[0]-leftmost[0])/2, topmost[1]+(bottommost[1]-topmost[1])/2)
    display_center = (int(true_center[0]), int(true_center[1]))
        
    return true_center, display_center

def trim_data(data_array, trim_from=0, trim_to=None):
    """Trims a np.array or all nested elements of a np.array to be the same length"""
    # remember the original shape, in case that was important
    original_shape = data_array.shape
    flattened = data_array.flatten()

    if trim_to is None:
        lengths = [len(data) for data in flattened]
        trim_to = min(lengths)

    for i, data in enumerate(flattened):
        flattened[i] = data[trim_from:trim_to]

    reshaped = flattened.reshape(original_shape)
    return reshaped

    
## ----------------- Contour Detection ----------------- ##

def detect_edges(image):
    edge_detected_image = cv2.Canny(image, 
                                    threshold1=30, 
                                    threshold2=130)
    
    return edge_detected_image

def find_points_on_rect(image, hsv_range, area_mm=12*6, image_section="upper_half"):
    """Function that returns the pixel-to-mm conversion and the four extreme points
        of a rectangle (left, right, top, bottom)
        Args: image - frame of video image capture or loaded cv2 image
              hsv_range - .npy
              area_mm - true area of detected rectangle
              image_section - what half of the image we're searching for the rectangle ("upper_half" or "lower_half")
        """

    # find the rectangle
    merged_contours = find_contours_rectangle(image, hsv_range, image_section)
    # compare the rectangle area in px to the known area in mm
    area_px = cv2.contourArea(merged_contours)
    pix_per_mm = np.sqrt(area_px/area_mm)

    # find the centerpoint of the detected rectangle (and display it for funsies)
    # sort by x and y
    reshaped_contours = merged_contours.reshape(-1,2)
    sort_dtype = [("x", int), ("y", int)]
    vals_to_sort = np.array([(x, y) for x,y in reshaped_contours], dtype=sort_dtype)
    sorted_x = np.sort(vals_to_sort, order="x")
    sorted_y = np.sort(vals_to_sort, order="y")
    # find the extreme points
    leftmost = sorted_x[0]
    rightmost = sorted_x[-1]
    topmost = sorted_y[0]
    bottommost = sorted_y[-1]

    return pix_per_mm, [leftmost, rightmost, topmost, bottommost]

## ----------------- Flight Code ----------------- ##

def calibrate(path_to_video, hsv_range):
    cap = cv2.VideoCapture(path_to_video)
    if (cap.isOpened()==False):
        print("Error opening video file")
    
    center_list = []
    pix_per_mm_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            resized_frame = resize_image(frame)
            pix_per_mm, extreme_points = find_points_on_rect(resized_frame, hsv_range) # <-- contours now in this function
            left, right, top, bottom = extreme_points
            true_center, display_center = find_rectangle_center(left, right, top, bottom)
            cv2.circle(resized_frame, display_center, 2, (255, 255, 0), 2)
            cv2.imshow("calibration", resized_frame)
            center_list.append(true_center)
            pix_per_mm_list.append(pix_per_mm)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop when the video finishes
        else:
            break
    # When everything is done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

    pix_per_mm_avg = np.average(pix_per_mm_list)
    center_avg = np.average(center_list, axis=0)

    return pix_per_mm_avg, center_avg

    
def video_capture(path_to_video, hsv_range, pix_per_mm, reference_point):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(path_to_video)
    
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")

    t = []
    y_dist_list = []
    # Read until video is completed
    while cap.isOpened():  
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            resized_frame = resize_image(frame)
            masked_frame = mask_image(resized_frame, hsv_range)
            cv2.imshow("mask", masked_frame)

            _, extreme_points = find_points_on_rect(resized_frame, hsv_range, image_section="lower_half")
            left, right, top, bottom = extreme_points
            true_center, display_center = find_rectangle_center(left, right, top, bottom)

            # the rightmost point happens to be pretty stable at the lower right corner, experiementing with
                # averaging its y coord and the bottommost y coord
            # center = (int(left[0]+(right[0]-left[0])/2), int((bottom[1]+right[1])/2))

            # display the points
            ref_point_display = (int(reference_point[0]), int(reference_point[1]))
            cv2.circle(resized_frame, ref_point_display, 2, (255,255,0), 2)
            cv2.circle(resized_frame, display_center, 2, (255,255,0), 2)
            cv2.circle(resized_frame, left, 2, (255, 0, 0), 2)
            cv2.circle(resized_frame, right, 2, (255, 0, 0), 2)
            cv2.circle(resized_frame, top, 2, (255, 0, 0), 2)
            cv2.circle(resized_frame, bottom, 2, (255, 0, 0), 2)

            cv2.line(resized_frame, display_center, ref_point_display, (0,255,255), 2)

            cv2.imshow("points", resized_frame)

            # find and save the y distance between the reference point and the detected center point
            y_dist_px = true_center[1] - reference_point[1]
            y_dist_mm = y_dist_px / pix_per_mm 
            y_dist_list.append(y_dist_mm)

            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            t.append(timestamp / 1000.0)
            
        # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop when the video finishes
        else:
            break
    # When everything is done, release the video capture object
    cap.release()
    # Closes all the frames
    cv2.destroyAllWindows()

    return t, y_dist_list

if __name__ == "__main__":
    # load the hsv value
    hsv_range = np.load("origami/hsv_value.npy")
    # load the video files
    folder_path = "origami\\media\\spring2\\"
    subfolders = ["6W", "8W"]

    data_means = []
    data_stdvs = []
    times = []
    for folder in subfolders:
        subfolder_data = []
        subfolder_times = []
        i=1
        for video in glob.glob(folder_path+folder+"\\*.mp4"):
            pix_per_mm, reference_point = calibrate(video, hsv_range)
            t, y_dist = video_capture(video, hsv_range, pix_per_mm, reference_point)
            subfolder_data.append(y_dist)
            subfolder_times.append(t)

            plt.plot(t, y_dist)
            # try:
            #     np.save(f"origami\\data\\spring2\\{folder}\\ydist_{i}.npy", y_dist)
            #     np.save(f"origami\\data\\spring2\\{folder}\\t_{i}.npy", t)
            # except:
            #     print("you spelled something wrong")
            #     np.save(f"ydist_{i}.npy", y_dist)
            #     np.save(f"t_{i}.npy", t)
            # i+=1

        plt.show()