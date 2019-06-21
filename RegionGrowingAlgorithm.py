import cv2
import numpy as np
import Queue as queue


class coor:
    x = 0
    y = 0

# img = cv2.imread('testFog.png', 0)
# img = cv2.Canny(img, 10, 100)
# cv2.imshow('Canny', img)
# cv2.waitKey(0)


X = 314 / 2
Y = 361 / 2 + 1

def get3n(x, y, shape):
    out = []
    maxx = shape[1]-1
    maxy = shape[0]-1

    #top left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    #top center
    outx = x
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    # top right
    outx = min(max(x+1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))
    return out


def region_growing(img, seed):
    out_img = img
    list = []

    # add [x last, y last]
    list.append((seed[0], seed[1]))

    # # Them cac pixel tu giua sang trai
    i = seed[0]
    while (img[seed[1], i] != 0):
        list.append((max(i - 1, 1), seed[1]))
        i = i - 1;
        # print i
    # Them cac pixel tu giua sang phai
    j = seed[0]
    while (img[seed[1], j] != 0):
        list.append((max(j + 1, 1), seed[1]))
        j = j + 1;
    processed = []

    # print max(y), max(x)
    print img.shape
    # get 3 zone above
    print get3n(seed[0], seed[1], img.shape)
    print len(list)
    while (len(list)>0):
        pix=list[0]
        out_img[pix[1],pix[0]]=255
        for coord in get3n(pix[0], pix[1], img.shape):
            lum_now = img[coord[1], coord[0]]
            lum_old = img[max(coord[1] - 1, 0), coord[0]]
            if (img[coord[1], coord[0]] != 0):
                out_img[coord[1], coord[0]] = 255
                if not coord in processed:
                    list.append(coord)
                processed.append(coord)
        # pop index 0 in list
        list.pop(0)
        cv2.imshow("progress",out_img)
        cv2.waitKey(1)
    return out_img

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Seed: ' + str(x) + ', ' + str(y) + '   Luminance: ' ,img[y,x]
        clicks.append((x,y))
clicks = []

image = cv2.imread('testFog.png', 0)
image = cv2.resize(image, (Y, X))
heigh, width = image.shape[:2]

print(heigh)
print(width)

ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)
# cv2.imshow('img', img)

# Ls = img[heigh-1, width/2]
# print Ls
# i = heigh-1
# j = width/2
# k = width/2
# edges = cv2.Canny(img, 20, 100)

edges = cv2.Canny(img, 20, 100)

# image = cv2.resize(image , (0, 0), fx = 0.25, fy = 0.25)
# img = cv2.resize(img , (0, 0), fx = 0.25, fy = 0.25)
# edges = cv2.resize(edges , (0, 0), fx = 0.25, fy = 0.25)
print "Debug HEHEEHEHEHEEHEH"
cv2.imshow('edges', edges)

indices = np.where(edges == 255)
coordinates = zip(indices[0], indices[1])
print coordinates
# To den cac vung canh
for i in range(0, len(coordinates)):
    # print coordinates[i]
    y = coordinates[i][0]
    x = coordinates[i][1]
    # cho nhung diem canh thanh mau den
    # nhung diem tren diem canh cung chuyen thanh mau den de tao thanh duong lien
    img[coordinates[i]] = 0
    img[min(y + 1, heigh - 1), x] = 0
#     # img[min(y+1, Y/2-1), x] = 0


cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0,)
cv2.imshow('Input', img)

cv2.waitKey(5000)
seed = clicks[-1]
print seed
out = region_growing(img, seed)
cv2.imwrite('output_file.png', out)

# heigh_out, width_out = out.shape[:2]
# B = []
# for i in range(0, heigh_out-1):
#     print 'line' + str(i)
#     dis = 0
#     temp = 0
#     begin = [i, 0]
#     end = [i, 0]
#     for j in range(0,width_out-1):
#         if (out[i, j] == 255):
#             temp = temp + 1
#             print 'temp' + str(temp)
#         else:
#             if (dis < temp):
#                 dis = temp
#                 end = [i, j - 1]
#                 begin = [i, j-temp]
#             temp = 0
#         # print j
#     # print 'dis' + str(dis)
#     # print begin
#     # print end
#     if (begin[1] == 0 and end[1] == 0):
#         end[1] = 360
#     B.append([begin, end])
# Lumi = []
# for i in range(0, heigh-1):
#     tong = 0
#     dis = B[i][1][1] - B[i][0][1] + 1
#     for j in range(B[i][0][1], B[i][1][1]):
#         tong = tong + image[i,j]
#     Lumi.append([i, tong/dis])
# print Lumi
cv2.imshow('Output', out)
cv2.waitKey()

