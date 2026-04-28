import sys, json
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None
        self.drawing = False
        self.rect_points = None
        self.finish = False
        self.setCursor(Qt.CrossCursor)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.end = self.start
            self.drawing = True
    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end = event.pos()
            self.update()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.finish:
            self.end = event.pos()
            self.drawing = False
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(), self.end.y()
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)
            self.rect_points =[(left, top),(right, top),(right, bottom),(left, bottom)]
            print("Points:",self.rect_points)
            data = {
                "points": [
                    {"x":left, "y":top},
                    {"x":right,"y": top},
                    {"x":right, "y":bottom},
                    {"x":left, "y":bottom}
               ],
                "image_size":{
                    "width": self.width(),
                    "height": self.height()
                }
            }
            with open("points.json","w") as f:
                json.dump(data, f)
            self.window().crop_second_image()
            self.update()
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.start and self.end:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 3))
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(), self.end.y()
            painter.drawRect(min(x1,x2),min(y1,y2),abs(x1 - x2),abs(y1-y2)) 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("rectangle")
        self.label = Label()
        img1 = QPixmap("/Users/atchayaramesh/Downloads/ball1.jpg")
        self.label.setPixmap(img1)
        self.label.setFixedSize(img1.size())
        self.setCentralWidget(self.label)
    def crop_second_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image")
        img2 = QPixmap(path)

        with open("points.json","r") as f:
            data = json.load(f)
        points = data["points"]
        size = data["image_size"]

        x1 = points[0]["x"]
        y1 = points[0]["y"]
        x2 = points[2]["x"]
        y2 = points[2]["y"]

        if img2.width() != size["width"] or img2.height() != size["height"]:
            print("Images are not same size")
        
        w = x2 - x1
        h = y2 - y1

        painter = QPainter(img2)
        painter.setPen(QPen(Qt.green, 3))
        painter.drawRect(x1, y1, w, h)
        painter.end()
        img2.save("output.jpg")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())