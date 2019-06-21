import cv2
import numpy as np


image = cv2.imread('fog_new.png', 0)
# print image

he, wi = image.shape[:2]
Y = wi
X = he

class coor:
    x = 0
    y = 0

# Chay theo 3 huong hoac 5 huong
d1 = [-1, -1, -1, 0, 0]
d2 = [-1, 0, 1, -1, 1]


# Ham BFS lan rong de tim vung Region Growing
# La vung the hien su lien thong tu mat duong len bau troi
def BFS(root, m):
    q = [root]
    m[root.x][root.y] = 255
    while q:
        n = q.pop()
        for i in range(3):
            next = coor()
            next.x = n.x + d1[i]
            next.y = n.y + d2[i]
            x1 = next.x
            y1 = next.y
            if (x1 >= 0 and x1 <= (X - 1) and y1 >= 0 and y1 <= (Y - 1) and m[x1][y1] != 0 and m[x1][y1] != 255):
                m[x1][y1] = 255;
                q.insert(0, next)



# Ham tim diem goc Seed Point
# La diem bat dau lan rong, thuong la diem chi mat dat
# def SeedPoint():

def FindSeedPoint(m):
    temp = m
    max = 0
    kq = 0
    for i in range(he-10, he-1, 1):
        dem = 0
        root = coor()
        root.x = i
        root.y = int(wi/2-1)
        q = [root]
        while q:
            dem = dem + 1;
            n = q.pop()
            for j in range(3,5):
                next = coor()
                next.x = n.x + d1[j]
                next.y = n.y + d2[j]
                x1 = next.x
                y1 = next.y
                if (x1 >= 0 and x1 <= (X - 1) and y1 >= 0 and y1 <= (Y - 1) and temp[x1][y1] == 0):
                    temp[x1][y1] = 255;
                    q.insert(0, next)
        if max<=dem:
            max = dem
            kq = i
    return kq

# def on_mouse(event, x, y, flags, params):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print 'Seed: ' + str(x) + ', ' + str(y) + '   Luminance: ', img[y, x]
#         clicks.append((x, y))
#
#
# clicks = []

image = cv2.resize(image, (Y, X))
heigh, width = image.shape[:2]

ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)

edges = cv2.Canny(img, 20, 100) # 20  ---- 80
# 90 -------- 200            DrivingInFog.jpg

# cv2.imshow('edges', edges)

indices = np.where(edges == 255)
coordinates = list(zip(indices[0], indices[1]))

# print coordinates
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

# Diem bat dau
seed = [int(wi/2-1), FindSeedPoint(edges)]
# print ("diem bat dau")
# print (seed[1])

# cv2.namedWindow('Input')
# cv2.setMouseCallback('Input', on_mouse, 0, )
# cv2.imshow('Input', img)

# cv2.waitKey(5000)
# print seed


def region_growing(img, seed):
    m = img
    list = []

    # add [x last, y last]
    list.append((seed[0], seed[1]))

    # # Them cac pixel tu giua sang trai
    i = seed[0]
    while (img[seed[1], i] != 0 and i>1):
        list.append((max(i - 1, 1), seed[1]))
        i = i - 1
        # print i
    # Them cac pixel tu giua sang phai
    j = seed[0]
    while (img[seed[1], j] != 0 and j<Y-1):
        list.append((max(j + 1, 1), seed[1]))
        j = j + 1

    # print max(y), max(x)
    # print img.shape
    # get 3 zone above
    # print len(list)

    # root = coor()
    # root.x = seed[0]
    # root.y = seed[1]
    # BFS(root, m)
    #
    # list.pop(0)
    # cv2.imshow("progress",m)
    # cv2.waitKey(1)
    while (len(list) > 0):
        pix = list[0]
        root = coor()
        root.x = pix[1]
        root.y = pix[0]
        BFS(root, m)

        list.pop(0)
        # cv2.imshow("progress", m)
        # cv2.waitKey(1)
    return m

def output():
    return region_growing(img, seed)
# result = output()
# cv2.imshow("region_growing", result)
# cv2.waitKey()
# out = region_growing(img, seed)
# cv2.imwrite('output_file.png', out)
#
# cv2.imshow('Output', out)
# cv2.waitKey()

