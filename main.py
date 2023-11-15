from PyQt5.QtWidgets import QApplication
import ui
import sys


app = QApplication(sys.argv)
win = ui.MyApp()
win.show()
sys.exit(app.exec_())