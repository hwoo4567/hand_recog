import sys
from PyQt5.QtWidgets import QApplication


screen = QApplication([]).primaryScreen()
size = screen.size()
width, height = size.width(), size.height()
print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
print('Available: %d x %d' % (rect.width(), rect.height()))