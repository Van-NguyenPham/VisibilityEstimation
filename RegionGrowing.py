# import cv2, cv
# import numpy as np
#
# def on_mouse(event, x, y, flags, params):
#     if event == cv.CV_EVENT_LBUTTONDOWN:
#         print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
#         s_box = x, y
#         boxes.append(s_box)
#
# def region_growing(img, seed):
#     #Parameters for region growing
#     neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     region_threshold = 0.2
#     region_size = 1
#     intensity_difference = 0
#     neighbor_points_list = []
#     neighbor_intensity_list = []
#
#     #Mean of the segmented region
#     region_mean = img[seed]
#
#     #Input image parameters
#     height, width = img.shape
#     image_size = height * width
#
#     #Initialize segmented output image
#     segmented_img = np.zeros((height, width, 1), np.uint8)
#
#     #Region growing until intensity difference becomes greater than certain threshold
#     while (intensity_difference < region_threshold) & (region_size < image_size):
#         #Loop through neighbor pixels
#         for i in range(4):
#             #Compute the neighbor pixel position
#             x_new = seed[0] + neighbors[i][0]
#             y_new = seed[1] + neighbors[i][1]
#
#             #Boundary Condition - check if the coordinates are inside the image
#             check_inside = (x_new >= 0) & (y_new >= 0) & (x_new < height) & (y_new < width)
#
#             #Add neighbor if inside and not already in segmented_img
#             if check_inside:
#                 if segmented_img[x_new, y_new] == 0:
#                     neighbor_points_list.append([x_new, y_new])
#                     neighbor_intensity_list.append(img[x_new, y_new])
#                     segmented_img[x_new, y_new] = 255
#
#         #Add pixel with intensity nearest to the mean to the region
#         distance = abs(neighbor_intensity_list-region_mean)
#         pixel_distance = min(distance)
#         index = np.where(distance == pixel_distance)[0][0]
#         segmented_img[seed[0], seed[1]] = 255
#         region_size += 1
#
#         #New region mean
#         region_mean = (region_mean*region_size + neighbor_intensity_list[index])/(region_size+1)
#
#         #Update the seed value
#         seed = neighbor_points_list[index]
#         #Remove the value from the neighborhood lists
#         neighbor_intensity_list[index] = neighbor_intensity_list[-1]
#         neighbor_points_list[index] = neighbor_points_list[-1]
#
#     return segmented_img
#
#
# if __name__ == '__main__':
#
#     boxes = []
#     filename = 'testFog.png'
#     img = cv2.imread(filename, 0)
#     img=cv2.cvtColor(img,cv2.COLOR_BAYER_BG2GRAY)
#     resized = cv2.resize(img,(256,256))
#     cv2.namedWindow('input')
#     cv2.setMouseCallback('input', on_mouse, 0,)
#     cv2.imshow('input', resized)
#     cv2.waitKey(5000)
#     print "Starting region growing based on last click"
#     seed = boxes[-1]
#     cv2.imshow('input', region_growing(resized, seed))
#     print "Done. Showing output now"
#
#     cv2.waitKey()
#     cv2.destroyAllWindows()



























import cv2
import numpy as np

def get8n(x, y, shape):
    out = []
    # y0 = shape[0]
    # x0 = shape[1]
    maxx = shape[1]-1
    maxy = shape[0]-1

    #top left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y-1,0),maxy)
    out.append((outx,outy))

    # #top center
    # outx = x
    # outy = min(max(y-1,0),maxy)
    # out.append((outx,outy))

    # #top right
    # outx = min(max(x+1,0),maxx)
    # outy = min(max(y-1,0),maxy)
    # out.append((outx,outy))
    #
    #left
    outx = min(max(x-1,0),maxx)
    outy = y
    out.append((outx,outy))

    # #right
    # outx = min(max(x+1,0),maxx)
    # outy = y
    # out.append((outx,outy))
    #
    # bottom left
    outx = min(max(x-1,0),maxx)
    outy = min(max(y+1,0),maxy)
    out.append((outx,outy))

    # #bottom center
    # outx = x
    # outy = min(max(y+1,0),maxy)
    # out.append((outx,outy))

    # #bottom right
    # outx = min(max(x+1,0),maxx)
    # outy = min(max(y+1,0),maxy)
    # out.append((outx,outy))
    return out

def region_growing(img, seed):
    list = []
    # tao 1 anh trang
    outimg = np.zeros_like(img)
    list.append((seed[0], seed[1]))
    processed = []
    print (len(list))
    while(len(list) > 0):
        pix = list[0]
        p_medium = img[pix[0], pix[1]]
        outimg[pix[0], pix[1]] = 255
        for coord in get8n(pix[0], pix[1], img.shape):
            # code lay vung theo 3 buoc
            # if img[coord[0], coord[1]] != 0:
            #     outimg[coord[0], coord[1]] = 255
            #     if not coord in processed:
            #         list.append(coord)
            #     processed.append(coord)

            # code lay vung theo 4 buoc
            if (img[coord[0], coord[1]] != 0 & (img[coord[0], coord[1]] - p_medium <= 3)):
                outimg[coord[0], coord[1]] = 255
                if not coord in processed:
                    list.append(coord)
                processed.append(coord)
        list.pop(0)
        # cv2.imshow("progress",outimg)
        # cv2.waitKey(1)
    return outimg

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('Seed: ' + str(x) + ', ' + str(y), img[y,x])
        clicks.append((y,x))

clicks = []
image = cv2.imread('testFog.png', 0)
# cv2.imshow('',image)
# image = cv2.Canny(image, 0.05, 100, apertureSize=3)

ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)
cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0, )
cv2.imshow('Input', img)
cv2.waitKey(5000)
seed = clicks[-1]
print (seed)
out = region_growing(img, seed)
cv2.imshow('Region Growing', out)
cv2.waitKey()
cv2.destroyAllWindows()
