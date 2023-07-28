import cv2
import numpy as np
  
def read_and_process_img(path_to_image):
    # Read image
    img = cv2.imread(path_to_image, cv2.IMREAD_COLOR)
    # Convert to grayscale
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel
    grey_blurred = cv2.blur(grey, (3, 3))

    return img, grey_blurred

def process_video_frame(frame):
    # Convert to grayscale
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur using 3 * 3 kernel
    grey_blurred = cv2.blur(grey, (3, 3))
    
    return grey_blurred

def detect_circles(image):

    # Apply Hough transform on the blurred image
    detected_circles = cv2.HoughCircles(image, 
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 30, minRadius = 70, maxRadius = 90)

    # detected_circles = cv2.HoughCircles(image, 
    #                 cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
    #             param2 = 30, minRadius = 90, maxRadius = 110)

  
    # Draw circles that are detected
    if detected_circles is not None:
    
        # Convert the circle parameters a, b and r to integers
        detected_circles = np.uint16(np.around(detected_circles))

        best_circle = detected_circles[0,:][0]

    else:
        best_circle = [0,0,0]

    print(best_circle)
    return best_circle
  
def display_circles(image, circles):    
    # for pt in circles:

    a, b, r = circles
    # a,b,r = pt[0], pt[1], pt[2]

    # print(r)

    # Draw the circumference of the circle
    cv2.circle(image, (a, b), r, (0, 255, 0), 2)

    # Draw a small circle (of radius 1) to show the center
    cv2.circle(image, (a, b), 1, (0, 0, 255), 3)
    cv2.imshow("Detected Circle", image)
    cv2.waitKey(0)

def video_capture(path_to_video):
    # Creating a VideoCapture object to read the video
    cap = cv2.VideoCapture(path_to_video)
 
    # Loop until the end of the video
    while (cap.isOpened()):
    
        # Capture frame-by-frame
        ret, frame = cap.read()
        # frame = cv2.resize(frame, fx = 0, fy = 0,
        #                     interpolation = cv2.INTER_CUBIC)
        
        frame = frame[300:700, 1000:1300]
        
        processed_frame = process_video_frame(frame)
        circles = detect_circles(processed_frame)
        display_circles(frame, circles)
    
        # Display the resulting frame
        # cv2.imshow('Frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
 
    # release the video capture object
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()

if __name__ == "__main__":
    path = 'donut-screenshot.png'
    vid_path = 'donut-video.mp4'

    img, processed_img = read_and_process_img(path)
    circles = detect_circles(processed_img)
    display_circles(img, circles)

    # video_capture(vid_path)