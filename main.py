
# cong thuc
# lamda = (a*H)/cos(phi)

# phi = 0 khi dat may anh thang dung, truc may anh song song mat dat
# H = chieu cao tu may anh den mat dat = 1.5 m
# a = f/tpu = f/tpv voi f la tieu cu, tpu = tpv = kich thuoc cua mot pixel

# camera:  https://www.xiaomiviet.vn/camera-hanh-trinh-g300-full-hd.html
# Thong so camera: https://shopee.vn/Camera-h%C3%A0nh-tr%C3%ACnh-Qihoo-360-Smart-Dash-Cam-G300-H%C3%A3ng-ph%C3%A2n-ph%E1%BB%91i-ch%C3%ADnh-th%E1%BB%A9c-i.97959351.1642325508
# f = 2.2 mm = 2.2 x 10^-3 m

# camera sensor: https://www.dipol.pt/camara_ip_compacta_signal_hdc-260p_2mp_2_8-12mm_0_01_lx_iv_ate_40m_h_265-h_264_poe__K1877.htm
# Thong so camera sensor: https://www.unifore.net/product-highlights/sony-imx323-cmos-image-sensor.html
# Hieu hon ve cac thong so: https://www.techspot.com/guides/850-smartphone-camera-hardware/page2.html

# tpu = tpv = 2.8 x 10^-6 m
import sys
import time
import RansacVanishingPoint
import InflectionPoint
import matplotlib.pyplot as plt
import cv2
start = time.time()
print ("bat dau: ")
ori = cv2.imread('fog_new.png')
a = (2.2/2.8)*1000
H = 1.5
lamda = a*H


DiemChanTroi = RansacVanishingPoint.VanishingPoint()
DiemUon = InflectionPoint.InflectionPoint

img = ori
height, width, channels = img.shape

# print (DiemUon)


# khoangcach = 3/k

cv2.line(img, (0, int (DiemChanTroi[1])), (width, int (DiemChanTroi[1])), (255, 0, 0), 1)

cv2.line(img, (0, DiemUon), (width, DiemUon), (0, 0, 255), 1)
vi = DiemUon # Tu file InflectionPoint
vh = int(DiemChanTroi[1]) # Tu file RansacVanishingPoint
d = int(-3*lamda/2/(vi-vh))

distance = "Tam nhin: "+str(d)+ " m"
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,distance,(int(width/3),int(height/7)), font, 2,(255,255,255),2,cv2.LINE_AA)
cv2.imshow("Anh ", img)
cv2.waitKey()
# plt.figure(figsize=(15,10))
# print (params[0])
# print (params[1])
# plt.imshow(img, cmap='gray')
# plt.plot(DiemChanTroi[0],DiemChanTroi[1],'+', markersize=1)
# plt.plot(DiemChanTroi[0], DiemUon, '*', markersize=1)
# plt.show()
print ("chan troi: ",int(DiemChanTroi[1]))
print ("diem uon:", int(DiemUon))
end = time.time()
print ("thoi gian chay: ",(end - start))
# print (khoangcach)




