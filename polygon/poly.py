import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.points = []
        self.finished = False
    def mousePressEvent(self, event):
        if self.finished:
            return
        if event.button() == Qt.LeftButton:
            point = event.pos()
            self.points.append(point)
            print(f"Point: ({point.x()}, {point.y()})")
            self.update()
        elif event.button() == Qt.RightButton:
            self.finished = True
            self.update()
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.points:
            return
        painter = QPainter(self)
        pen = QPen(Qt.red,2)
        painter.setPen(pen)

        for p in self.points:
            painter.drawEllipse(p, 3, 3)
            
        for i in range(len(self.points) -1):
            painter.drawLine(self.points[i], self.points[i+1])

        if self.finished and len(self.points) > 2:
            painter.drawLine(self.points[-1], self.points[0])
           
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polygon draw")
        self.label = Label()
        pixmap = QPixmap("/Users/atchayaramesh/Downloads/ball1.jpg")
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())