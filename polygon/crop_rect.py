import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.start = None
        self.end = None
        self.drawing = False
        self.rect_points =  None
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
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.drawing = False
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(), self.end.y()
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)
            self.rect_points = [(left, top),(right, top),(right, bottom),(left,bottom)]
            print("Points:", self.rect_points)
            self.crop_second_image()
            self.update()

    def crop_second_image(self):
        if not self.rect_points:
            return
        pixmap2 = QPixmap("/Users/atchayaramesh/Downloads/ball2.jpg")
        x1, y1 = self.rect_points[0]
        x2, y2 = self.rect_points[2]
        w = x2 - x1
        h = y2 - y1
        painter = QPainter(pixmap2)
        painter.setPen(QPen(Qt.green, 3))
        painter.drawRect(x1, y1, w, h)
        for (x, y) in self.rect_points:
            painter.drawEllipse(x, y, 5, 5)

        painter.end()

        second_points = [(x1, y1),(x2,y1),(x2,y2),(x1,y2)]
        print("second image Points")
        for p in second_points:
            print(p)
        pixmap2.save("output_marked.jpg")
        
        print("image saved")
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.start and self.end:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red,3))
            x1, y1 = self.start.x(), self.start.y()
            x2, y2 = self.end.x(),self.end.y()
            rect_x = min(x1, x2)
            rect_y = min(y1, y2)
            width = abs(x1 - x2)
            height = abs(y1 - y2)
            painter.drawRect(rect_x, rect_y, width, height)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rectangle")
        self.label = Label()
        pixmap = QPixmap("/Users/atchayaramesh/Downloads/ball1.jpg")
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(pixmap.size())
        self.setCentralWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())