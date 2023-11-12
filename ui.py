import typing
from PyQt5 import QtCore, QtGui
import cv2
import threading
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import (
    QImage,
    QPixmap,
    # event
    QCloseEvent,
)
from PyQt5.QtCore import *

running = False

def runCamera(video_label: QLabel):
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video_label.resize(int(width), int(height))
    
    while running:
        ret, img = cap.read()
        
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            h,w,c = img.shape

            qImg = QImage(img.data, w, h, w*c, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            video_label.setPixmap(pixmap)
        else:
            QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")

        break

    cap.release()
    print("Thread end.")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Hand Recog")
        self.move(300, 300)
        self.resize(400, 200)
        
        vbox = QVBoxLayout()
        self.video_label = QLabel()
        btn_start = QPushButton("Camera On")
        btn_stop = QPushButton("Camera Off")

        vbox.addWidget(self.video_label)
        vbox.addWidget(btn_start)
        vbox.addWidget(btn_stop)
        self.setLayout(vbox)
        self.show()

        btn_start.clicked.connect(self.startCamera)
        btn_stop.clicked.connect(self.stopCamera)

        self.show()

    def startCamera(self):
        global running
        running = True
        th = threading.Thread(target=lambda: runCamera(self.video_label))
        th.start()
        print("started..")
        
    def stopCamera(self):
        global running
        running = False
        print("stoped..")

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        print("exit")


if __name__ == "__main__":
    app = QApplication([])
    win = MyApp()
    sys.exit(app.exec_())