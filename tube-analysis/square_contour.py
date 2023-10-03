import numpy as np
import cv2
import matplotlib.pyplot as plt

hsv_range = np.load("hsv_value.npy")

def crop_image(image):
    # crop: img[y:y+h, x:x+w]
    dimensions = image.shape
    height = dimensions[0]
    width = dimensions[1]

    w_margin = int(width/4)
    h_start = int(height/4)
    cropped = image[h_start:height, w_margin:(width-w_margin)]
    return cropped

def edge_image(image):
    blurred = cv2.blur(image, (3, 3))
    hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, hsv_range[0], hsv_range[1])
    edge = cv2.Canny(mask, 150, 300, L2gradient=True)
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

img = cv2.imread("media/shell_screenshot.png")
vid_path = "media/shell_10-3.mp4"

# cap = cv2.VideoCapture(vid_path)
# count = 0
# fps = 30

# area_list = []
# t = []

# while (cap.isOpened()):
#     ret, frame = cap.read()
#     # do processing if video still has frames left
#     if ret:
#         # grab a frame every second (residual is zero)
#         if count%1==0:
#             # cv2.imshow("raw", frame)
#             frame = crop_image(frame)
#             edges = edge_image(frame)
#             cv2.imshow("edge", edges)

#             timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
#             t.append(timestamp / 1000.0)

#             contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             merged_contours = merge_contours(contours)
#             area = cv2.contourArea(merged_contours)
#             area_list.append(area)

#             cv2.drawContours(frame, [merged_contours], -1, (0, 255, 0), 2)
#             cv2.imshow("contours", frame)
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

# area_list = np.load("area_pix_10-3.npy")
# t = np.load("t.npy")

# fig, ax = plt.subplots(1,1)
# ax.plot(t, area_list)
# plt.show()