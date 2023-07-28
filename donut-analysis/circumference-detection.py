import numpy as np
import cv2
import matplotlib.pyplot as plt

# HSV mask values
blue_min = np.array([95, 60, 51],np.uint8)
blue_max = np.array([120, 255, 255],np.uint8)

def read_and_crop(path, display=False):
    img = cv2.imread(path)

    # crop image
    img = img[300:700, 500:900]

    if display == True:
        cv2.imshow("raw image", img)
        cv2.waitKey(0)

    return img

def mask_image(image, display=False):
    blurred = cv2.blur(image, (5, 5))
    hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    masked_img = cv2.inRange(hsv_img, blue_min, blue_max)
    
    if display == True:
        cv2.imshow('hsv mask', masked_img)
        # cv2.waitKey(0)

    return masked_img

def detect_edges(image, display=False):

    edge_detected_image = cv2.Canny(image, 
                                    threshold1=100, 
                                    threshold2=200)
    
    if display == True:
        cv2.imshow('canny edge detection', edge_detected_image)
        # cv2.waitKey(0)

    return edge_detected_image

def detect_contours(raw_image, edge_image, display=False):

    contours, hierarchy = cv2.findContours(edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # only accept circular contours https://www.authentise.com/post/detecting-circular-shapes-using-contours
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if ((len(approx) > 8) & (area > 80) & (perimeter > 500) & (perimeter < 800)):
            contour_list.append(contour)

    if display == True:
        cv2.drawContours(raw_image, contour_list,  0, (255,0,0), 2)
        cv2.imshow('Objects Detected', raw_image)
        # cv2.waitKey(0)

    return contours, contour_list

def find_contour_perimeter(contour):
    perimeter = cv2.arcLength(contour, True)
    print(f"Countour perimeter: {perimeter} pixels")
    return perimeter

def merge_contours(contour_list):
    list_of_pts = [] 
    for contour in contour_list:
        list_of_pts += [pt for pt in contour]

    formatted_pts = np.array(list_of_pts).reshape((-1,1,2)).astype(np.int32)
    merged_contour = cv2.convexHull(formatted_pts)
    return merged_contour

def video_capture(path_to_video):

    cap = cv2.VideoCapture(path_to_video)
    circumference = []
 
    # Loop until the end of the video
    while (cap.isOpened()):
    
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # frame = cv2.resize(frame, fx = 0, fy = 0,
            #                     interpolation = cv2.INTER_CUBIC)
            
            frame = frame[300:700, 1000:1300]
            
            masked_frame = mask_image(frame)
            edges = detect_edges(masked_frame)


            cv2.imshow("mask", masked_frame)
            cv2.imshow("edges", edges)

            contour_list_raw, contour_list_filtered = detect_contours(raw_image=frame, edge_image=edges)
            if len(contour_list_filtered) != 0:
                merged_contours = merge_contours(contour_list_filtered)
                perimeter = cv2.arcLength(merged_contours, False)
                circumference.append(perimeter)
                # print(f"number of contours: {len(merged_contours)}")
                # print(f"perimeter: {perimeter}")
                cv2.drawContours(frame, merged_contours, -1, (255,0,0), 2)
                cv2.imshow('Objects Detected', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return circumference
        else:
            # release the video capture object
            cap.release()
            # Closes all the windows currently opened.
            cv2.destroyAllWindows()
            return circumference
            

    return circumference

if __name__ == "__main__":
    img_path = "donut-screenshot.png"
    vid_path = "donut-video.mp4"

    circumference_list = video_capture(vid_path)
    x = np.linspace(0, 94, len(circumference_list))

    fig, ax = plt.subplots(1,1)
    ax.plot(x, circumference_list)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Circumference (pixel)")
    plt.show()

    # raw_image = read_and_crop(path)
    # mask = mask_image(raw_image)
    # edge_image = detect_edges(mask)
    # contour_list = detect_contours(raw_image, edge_image)
    # perimeter = find_contour_perimeter(contour_list[0])