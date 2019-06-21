from __future__ import division
from scipy.interpolate import spline
import cv2
import numpy as np
import matplotlib.pyplot as plt

import RegionGrowingBFS

in_image = cv2.imread('fog_new.png', 0)
# in_image = RegionGrowingBFS.image
heigh, width = in_image.shape[:2]
Y = width
X = heigh

out_file = RegionGrowingBFS.output()

# mang B chua cac diem anh mau trang la region_growing
B = []
for i in range(0, heigh-1):
    # print 'line' + str(i)
    dis = 0
    temp = 0
    begin = 0
    end = 0
    for j in range(0,width):
        if (out_file[i, j] == 255):
            # print 'temp' + str(temp)
            temp = temp + 1
        else:
            if (dis < temp):
                dis = temp
                end = j - 1
                begin = j - temp
                temp = 0
            temp = 0
    # print 'dis' + str(dis)
    # print begin
    # print end
    if (begin == 0 and end == 0):
        end = width - 1
        dis = width - 1
    B.append([i, begin, end, end - begin + 1])
# print B

# image = cv2.imread('DrivingInFog.jpg', 0)
#
#
# cv2.imshow("anh goc: ", in_image)
# cv2.waitKey()

# m = in_image
# # Hien thi anh bang thong B
# for i in range(0, len(B)):
#     for j in range(B[i][1], B[i][2] + 1):
#         m[i][j] = 255
# cv2.imshow("Anh sau: ", m)
# cv2.waitKey()


luminance = []

# print B[533]
# print "DEBUG"
# tong = 0
# for j in range(B[533][1], B[533][2] + 1):
#     tong = tong + in_image[i][j]
# print tong/B[533][3]

for i in range(0, len(B)):
    tong = 0
    for j in range(B[i][1], B[i][2] + 1):
        tong = tong + in_image[i][j]
    luminance.append([i, tong / B[i][3]])

axisx = []
axisy = []
deriy = []
# print (luminance)
# print luminance
size = len(luminance)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
for i in range(0, len(luminance)):
    axisx.append(luminance[i][0])
    axisy.append(luminance[i][1])
# mang xnew [0, X, do chia nho nhat la 1]
xnew = np.linspace(axisx[0], axisx[X - 2], X - 1, endpoint=True)
power_smooth = spline(axisx, axisy, xnew)


min = 9999
InflectionPoint = 0
# tinh dao ham
y_new = []
y_new.append(0)
for j in range(1, size - 1):
    if min > ((axisy[j+1]-axisy[j-1])/2):
        min = (axisy[j+1]-axisy[j-1])/2
        InflectionPoint = j
    y_new.append((axisy[j+1]-axisy[j-1])/2)
y_new.append(0)
# plt.plot(xnew, axisy, color='red'),
# plt.plot(xnew, smooth(axisy, 13), 'g-', lw=2)
# plt.axis([0, X-1, 0, 250])
# plt.xlabel('Bandwidth Heigh (Image Heigh)')
# plt.ylabel('Intensity Value')
#
# 
# he, wi = out_file.shape
# print (InflectionPoint)
# cv2.line(out_file, (int (wi/2-1+20),int (InflectionPoint)), (int (wi/2-1+20),int (InflectionPoint)), (0, 0, 255), 10)
# cv2.imshow("InflectionPoint", out_file)
# cv2.waitKey()

# print y_new
# plt.plot(xnew, y_new, color='blue')
# plt.axis([0,Y-1, -5 , 2])
# plt.show()

# cv2.waitKey(0)