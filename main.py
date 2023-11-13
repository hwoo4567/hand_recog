from PyQt5.QtWidgets import QApplication
import ui
import hand
import sys


app = QApplication(sys.argv)
win = ui.MyApp()
sys.exit(app.exec_())