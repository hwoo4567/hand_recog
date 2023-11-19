from PyQt5.QtWidgets import QApplication
import win32api
import win32con

left, right, middle = False, False, False
fps = 1 / 60

def get_screen_size():
    screen = QApplication.desktop().screenGeometry()
    width, height = screen.width(), screen.height()
    return width, height

def moveTo(x, y):
    win32api.SetCursorPos((x, y))

def mouseDown(button):
    global left, right, middle
    
    x, y = win32api.GetCursorPos()
    if button == "left" and not left:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        left = True
    if button == "right" and not right:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        right = True
    if button == "middle" and not middle:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
        middle = True
    
def mouseUp(button):
    global left, right, middle
    
    x, y = win32api.GetCursorPos()
    if button == "left" and left:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        left = False
    if button == "right" and right:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        right = False
    if button == "middle" and middle:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)
        middle = False

if __name__ == "__main__":
    import time
    time.sleep(2)
    moveTo(*get_screen_size())
    mouseDown("left")
    mouseUp("left")