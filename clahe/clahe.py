import cv2
import matplotlib.pyplot as plt
img = cv2.imread("/Users/atchayaramesh/Downloads/street1.jpg")
image_resize = cv2.resize(img , (600, 400))
gray = cv2.cvtColor(image_resize, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit= 5, tileGridSize=(8,8))
clahe_img = clahe.apply(gray)
clahe_bgr = cv2.cvtColor(clahe_img, cv2.COLOR_GRAY2BGR)

plt.figure(figsize=(10,5))
plt.subplot(2,2,2)
plt.title("gray image")
plt.imshow(gray, cmap='gray')
plt.axis('off')

plt.subplot(2,2,4)
plt.title("clahe image")
plt.imshow(clahe_img, cmap='gray')
plt.axis('off')
equalized = cv2.equalizeHist(gray)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
clahe_hsv = cv2.createCLAHE(2.5,tileGridSize=(8,8))
clahe_v = clahe.apply(v)
hsv_clahe = cv2.merge((h,s,clahe_v))

clahe_clr = cv2.cvtColor(hsv_clahe,cv2.COLOR_HSV2BGR)
#cv2.imshow("clahe clr", clahe_clr)
#cv2.waitKey(0)
plt.subplot(2,2,3)
plt.title("clahe clr")
clahe_rgb = cv2.cvtColor(clahe_clr,cv2.COLOR_BGR2RGB)
plt.imshow(clahe_rgb)
plt.axis('off')

plt.subplot(2,2,1)
plt.title("original image")
img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.axis('off')

plt.savefig("mat.jpg")
plt.show()