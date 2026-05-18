import cv2
import numpy as np
import winsound
class ColorDetection:
    def __init__(self, image_path, color_name, lower, upper,lower2=None, upper2=None):
        self.image = cv2.imread(image_path)
        self.image = cv2.resize(self.image, (400, 400))
        self.color_name = color_name
        self.lower = np.array(lower)
        self.upper = np.array(upper)
        self.lower2 = np.array(lower2) if lower2 else None
        self.upper2 = np.array(upper2) if upper2 else None
    def detect_color(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, self.lower, self.upper)
        if self.lower2 is not None:
            mask2 = cv2.inRange(hsv, self.lower2, self.upper2)
            self.mask = mask1 + mask2
        else:
            self.mask = mask1
        self.result = cv2.bitwise_and(self.image,self.image, mask=self.mask)
        self.mask_bgr = cv2.cvtColor(self.mask, cv2.COLOR_GRAY2BGR)
        if self.color_name == "Red":
            print("Danger!Red detected,Something happened")
            winsound.Beep(1000, 1000)
            cv2.putText(self.result,"DANGER",(20, 350),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255, 255),2)
        elif self.color_name == "Amber":
            cv2.putText(self.result,"WARNING / CAUTION",(20, 350),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)
        elif self.color_name == "Green":
            cv2.putText(self.result,"SAFE CONDITION",(20, 350),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)
    def add_text(self):
        cv2.putText(self.image,"Original Image",(20, 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 0,0),2)
        cv2.putText(self.mask_bgr,f"{self.color_name} Mask",(20, 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0, 255),2)
        cv2.putText(self.result,f"{self.color_name} Detection",(20, 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 255),2)
    def display(self):
        img1 = cv2.copyMakeBorder(self.image,10, 10, 10, 10,cv2.BORDER_CONSTANT,value=(255, 255, 255))
        img2 = cv2.copyMakeBorder(self.mask_bgr,10, 10, 10, 10,cv2.BORDER_CONSTANT,value=(255, 255, 255))
        img3 = cv2.copyMakeBorder(self.result,10, 10, 10, 10,cv2.BORDER_CONSTANT,value=(255, 255, 255))
        final = np.hstack((img1, img2, img3))
        cv2.imshow(f"{self.color_name} Detection", final)
green = ColorDetection(r"C:\picture\green light.png","Green",[40, 50, 50],[80, 255, 255])
amber = ColorDetection(r"C:\picture\amber light.png","Amber",[15, 120, 120],[35, 255, 255])
red = ColorDetection(r"C:\picture\red light.jpg","Red",[0, 120, 70],[10, 255, 255],[170, 120, 70],[180, 255, 255])
objects = [green, amber, red]
for obj in objects:
    obj.detect_color()
    obj.add_text()
    obj.display()
cv2.waitKey(0)
cv2.destroyAllWindows() 