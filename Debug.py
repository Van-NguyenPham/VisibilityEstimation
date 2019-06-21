import cv2

image = cv2.imread('fog_new.png', 0)
he, wi = image.shape[:2]

print he-1
print wi/2-1



ret, img = cv2.threshold(image, 188, 255, cv2.THRESH_TRUNC)

# cv2.imshow("Anh", image)
# cv2.waitKey()
edges = cv2.Canny(img, 20, 200) # 20  ---- 80
# 90 -------- 200            DrivingInFog.jpg

# for i in range (he-1, he-151, -1):


cv2.imshow('edges', edges)
cv2.waitKey()

print image[he-1][wi/2-1]