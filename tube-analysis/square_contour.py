import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt

hsv_range = np.load("hsv_value.npy")

def crop_image(image):
    # crop: img[y:y+h, x:x+w]
    dimensions = image.shape
    height = dimensions[0]
    width = dimensions[1]

    w_start = int(width/3.2)
    w_stop = int(width/1.38)

    h_start = int(height/8)
    h_stop = int(height/1.25)

    cropped = image[h_start:h_stop, w_start:w_stop]
    return cropped

def edge_image(image):
    blurred = cv2.blur(image, (3, 3))
    hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
    # v = np.median(image)
    # sigma = 0.7
    # lower = int(max(0, (1.0 - sigma) * v))
    # upper = int(min(255, (1.0 + sigma) * v))
    lower = 50
    upper = 100
    edge = cv2.Canny(mask, lower, upper, L2gradient=True)
    return edge

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

def calibrate(contours):

    x_vals = np.array([point[0][0] for point in contours])
    # y_vals = np.array([point[0][1] for point in contours])

    left = contours[x_vals.argmin()][0]
    right = contours[x_vals.argmax()][0]

    width = np.abs(right[0] - left[0])
    print(f"length in px: {width}")

    true_width = 34.3 # mm
    pix_per_mm = width / true_width

    return left, right, pix_per_mm


def area_from_video(vid_path):

    cal_flag = True
    area_list = []
    t = []

    cap = cv2.VideoCapture(vid_path)

    while (cap.isOpened()):
        ret, frame = cap.read()
        # do processing if video still has frames left
        if ret:
            # cv2.imshow("raw", frame)
            frame = crop_image(frame)
            edges = edge_image(frame)
            cv2.imshow("edge", edges)

            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            t.append(timestamp / 1000.0)

            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            merged_contours = merge_contours(contours)

            if cal_flag == True:
                left, right, pix_per_mm = calibrate(merged_contours)
                cal_flag = False

            pix_per_mm2 = pix_per_mm**2
            area_px = cv2.contourArea(merged_contours)
            area = area_px / pix_per_mm2
            if area > 1350:
                area = None
            area_list.append(area)

            cv2.line(frame, left, right, (255,0,0), thickness=1)
            cv2.drawContours(frame, [merged_contours], -1, (0, 255, 0), 2)
            cv2.imshow("contours", frame)

            # cleanup if manually ended ("q" key pressed)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
        
        # cleanup if video ends
        else:
            cap.release()
            cv2.destroyAllWindows()

    return area_list, t

def remove_outliers(data):

    # cutoff = [40, 40]
    for _ in range(5):
        for i, point in enumerate(data[0:-1]):
            next_point = data[i+1]
            prev_point = data[i-1]
            
            # decreasing portion: if it's an outlier
            if prev_point - point > 20:
                data[i] = prev_point

            if next_point-point > 8:
                data[i] = prev_point
            

        # first point
    if data[0] - data[1] < 15:
        data[0] = data[1]

    return data

# folder_list = ["all-on", "pulse-hold", "pulse-release"]


folder_list = ["pulse-release"]
video_names = ["1.mp4"]
save_name = [str(video_names[0][0])]
video_names = ["1", "2", "3"]

fig, ax = plt.subplots(1,1)

for folder in folder_list:
    for i, video in enumerate(video_names):
        # path = "media/tube/"+folder+"/"+video
        # area_list, t = area_from_video(path)
        # np.save("data/tube/"+folder+"/"+save_name[i]+"-area.npy", np.array(area_list))
        # np.save("data/tube/"+folder+"/"+save_name[i]+"-t.npy", np.array(t))

        area_list = np.load("data/shell/"+folder+"/"+video+"-area.npy", allow_pickle=True)
        t = np.load("data/shell/"+folder+"/"+video+"-t.npy", allow_pickle=True)

        # area_list = remove_outliers(area_list)
        
        ax.plot(t, area_list, '.', label=video)

ax.legend(loc=0)
plt.show()