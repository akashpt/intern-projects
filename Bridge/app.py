import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QThread
from classes.bridge import Bridge

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bridge")
        self.resize(800, 600)
        
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)

        self.bridge = Bridge()
        
        self.thread = QThread()
        self.bridge.moveToThread(self.thread)
        self.thread.start()

        self.bridge.startCamera()
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.view.page().setWebChannel(self.channel)

        file_path = Path("templates/index.html").resolve()
        self.view.load(QUrl.fromLocalFile(str(file_path)))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())