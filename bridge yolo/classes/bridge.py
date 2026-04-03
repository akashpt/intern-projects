from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import cv2, base64, time
from threading import Thread
from ultralytics import YOLO
from yolo import detect_objects

class Bridge(QObject):
    frame_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.cap = None
        self.frames = []
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
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.lastest_frame = frame
            
            _, buffer = cv2.imencode(".jpg",frame)
            img_str = base64.b64encode(buffer).decode("utf-8")
            self.frame_signal.emit(img_str)
            
    def process_frame(self):
        while self.running:
            if self.lastest_frame is None:
                continue
            current_time = time.time()
            if current_time - self.last_process_time >= 0.2:
                self.last_process_time = current_time

                frame = self.lastest_frame
                processed_frame = detect_objects(frame)
                _, buffer = cv2.imencode(".jpg", processed_frame)
                img_str = base64.b64encode(buffer).decode("utf-8")
                self.frames.append(img_str)
                self.frame_signal.emit(img_str)
                resize = cv2.resize(processed_frame,(500,350))
                cv2.imwrite("output.jpg", resize)
            time.sleep(1)

    @pyqtSlot()
    def stopCamera(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        for img in self.frames:
            self.frame_signal.emit(img)