import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
sys.path.append("C:\\Users\\alicl\\Documents\\GitHub\\salp-research")
from create_paper_figure import MakePlot

def find_minor_dia(maj_dia_mm, ellipse_axes):
    maj_dia_px = ellipse_axes[0]
    min_dia_px = ellipse_axes[1]
    min_dia_mm = min_dia_px * maj_dia_mm / maj_dia_px
    return min_dia_mm

# img = cv2.imread("media/shell/front/half-contraction-20s.png")
img = cv2.imread("media/tube-no-contraction.jpg")
resized = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)

# crop: img[y:y+h, x:x+w]
# y = int(resized.shape[1])
# x = int(resized.shape[0]/3)
# cropped = resized[0:y, x:(-1-x)]

# dims = cropped.shape
dims = resized.shape
width = dims[0]
height = dims[1]

# center = (int(height/2-30), int(width/2+35))
center= (int(height/2+10), int(width/2+10))

maj_dia_px = 210
min_dia_px = 80
axes = (maj_dia_px, min_dia_px)
# print(axes)

angle=80
startAngle=0
endAngle=360
color=(0,255,0)
thickness=4
                 
# ellipse = cv2.ellipse(cropped, center, axes, angle, startAngle, endAngle, color, thickness) 
# cv2.imshow("shell front", ellipse)
circle = cv2.circle(resized, center, 130, color, thickness)
cv2.imshow("tube front", circle)
cv2.waitKey(0)

shell_front_area = np.load("data/averages/shell_all-on_avg.npy")
l = 34.3
no_contraction = np.mean(shell_front_area[0:5*30]) / l
full_contraction = min(shell_front_area) / l
med_contraction = shell_front_area[20*30] / l
maj_diameters = [no_contraction, med_contraction, full_contraction]

maj_dia_mm = maj_diameters[1]
min_dia_mm = find_minor_dia(maj_dia_mm, axes)
print(maj_dia_mm, min_dia_mm)
