from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import cv2
import base64
import numpy as np
import time
from threading import Thread

class Bridge(QObject):
    frame_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.cap = None
        self.frames = []
        self.total_white = 0
        self.total_black = 0
        self.running = False
        self.lastest_frame = None
        self.last_process_time = 0
      
    @pyqtSlot()
    def startCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True
        
        Thread(target=self.capture_loop, daemon = True).start()
        Thread(target=self.process_frame, daemon = True).start()

    def capture_loop(self):
        while self.running == True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            self.lastest_frame = frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, buffer =cv2.imencode(".jpg", gray)
            img_str = base64.b64encode(buffer).decode("utf-8")
            self.frame_signal.emit(img_str)
            
    def process_frame(self):
            while self.running:
                if self.lastest_frame is None:
                    continue

                current_time = time.time()
                if current_time - self.last_process_time >= 0.1:
                    self.last_process_time = current_time
                    
                    frame = self.lastest_frame
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    blur = cv2.GaussianBlur(gray,(5,5),0)
                    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    _, buffer =cv2.imencode(".jpg", gray)
                    img_str = base64.b64encode(buffer).decode("utf-8")
                    self.frames.append(img_str)
                    self.frame_signal.emit(img_str)
                    white_pixel = np.sum(binary == 255)
                    black_pixel = np.sum(binary == 0)
                    self.total_white += white_pixel
                    self.total_black += black_pixel
                    with open("output.txt", "w") as f:
                        f.write(f"White pixels:{self.total_white}\n")
                        f.write(f"Black pixels:{self.total_black}\n")
                time.sleep(2)
           
    @pyqtSlot()
    def stopCamera(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None

        for img in self.frames:
            self.frame_signal.emit(img)
