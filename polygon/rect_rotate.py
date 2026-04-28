import sys, json, math
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None
        self.drawing = False
        self.rect = []
        self.finished = False
        self.setCursor(Qt.CrossCursor)
        self.setFocusPolicy(Qt.StrongFocus)
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
        if event.button() == Qt.LeftButton and not self.finished:
            if len(self.rect) == 7:
                return
            self.end = event.pos()
            self.drawing = False
            
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(), self.end.y()

            dx = x2 - x1
            dy = y2 - y1

            length = math.sqrt(dx*dx + dy*dy)
            if length == 0:
                return
            ux = dx / length
            uy = dy / length
            px = -uy
            py = ux
           
            width = (y2 - y1)
            
            if abs(width) < 10:
                width = 10 if width >= 0 else -10
            rect = [
                (x1, y1),
                (x2, y2),
                (x2 - px * width, y2 - py * width),
                (x1 - px * width, y1 - py * width)
            ]
            #rect = [(left, top),(right, top),(right,bottom),(left, bottom)]
            self.rect.append(rect)
            #print("rectangles:", self.rect)
            self.update()

            if len(self.rect) == 7:
                self.finished = True
                self.start = None
                self.end = None
                self.update()

                data = {
                    "rectangles": [],
                    "image_size": {
                        "width": self.width(),
                        "height": self.height()
                }
            }
                for rect in self.rect:
                    points_list = []
                    for p in rect:
                        points_list.append({"x": p[0], "y": p[1]})
                    data["rectangles"].append(points_list)
                with open("points.json","w") as f:
                    json.dump(data, f, indent=4)
                self.window().crop_second_image() 

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            if self.rect:
                self.rect.pop()
                self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 3))
        for rect in self.rect:
            points = [QPoint(int(p[0]), int(p[1])) for p in rect]
            painter.drawPolygon(QPolygon(points))
        if self.start and self.end and self.drawing:
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(), self.end.y()

            dx = x2 - x1
            dy = y2 - y1

            length = math.sqrt(dx*dx + dy*dy)
            if length == 0:
                return

            ux = dx / length
            uy = dy / length

            px = -uy
            py = ux

            width = (y2 - y1)
            if abs(width) < 10:
                width = 10 if width >= 0 else -10

            rect = [
                (x1, y1),
                (x2, y2),
                (x2 - px * width, y2 - py * width),
                (x1 - px * width, y1 - py * width)
            ]
            points = [QPoint(int(p[0]), int(p[1])) for p in rect]
            painter.drawPolygon(QPolygon(points))
 

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
        rectangles = data["rectangles"]
        size = data["image_size"]
        
        if img2.width() != size["width"] or img2.height() != size["height"]:
            print("Image are not same size")
        
        painter = QPainter(img2)
        painter.setPen(QPen(Qt.red, 3))
        for rect in rectangles:
            points = []
            for p in rect:
                x = int(p["x"])
                y = int(p["y"])
                points.append(QPoint(x, y))
            polygon = QPolygon(points)
            painter.drawPolygon(polygon)
        painter.end()
        img2.save("output_rect.jpg")
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())