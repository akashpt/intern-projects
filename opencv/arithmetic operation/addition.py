import cv2
from matplotlib import pyplot as plt
img1 = cv2.imread(r"C:\picture\square.jpg")
img2 = cv2.imread(r"C:\picture\circle.jpg")
added = cv2.add(img1, img2)
plt.imshow(added)
plt.title("Added Image")
plt.axis("off")
plt.show()