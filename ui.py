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
from PyQt5.QtCore import (
    Qt,
    QTimer,
)

import cam

class MyApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Hand Recog")
        self.move(100, 100)
        self.resize(500, 400)
        
        vbox = QVBoxLayout()
        self.video_label = QLabel()
        self.info_label = QLabel(text="...")
        btn_start = QPushButton("Camera On")
        btn_stop = QPushButton("Camera Off")

        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.video_label)
        vbox.addWidget(self.info_label)
        vbox.addWidget(btn_start)
        vbox.addWidget(btn_stop)
        self.setLayout(vbox)

        btn_start.clicked.connect(self.startCamera)
        btn_stop.clicked.connect(self.stopCamera)
        
        # 카메라 업데이트를 위한 타이머 설정
        w, h = cam.startCam()
        self.video_label.resize(w, h)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_by_frame)

    def startCamera(self):
        if not self.timer.isActive():
            self.timer.start(1000 // 30)  # 매 1/30초마다 업데이트
            print("cam on..")
        
    def stopCamera(self):
        self.timer.stop()
        print("cam stopped..")
        
    def update_by_frame(self):
        cam.init()
        cam.controlMouseByFrame()
        
        info = cam.getInfo()
        self.info_label.setText(info)

        img = cam.getFrame(show_margin=True)
        if img is None:
            QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            return
            
        h, w, c = img.shape
        qImg = QImage(img.data, w, h, w*c, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, e: QCloseEvent | None) -> None:
        self.stopCamera()
        cam.closeCam()
        print("exit")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())