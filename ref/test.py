import win32api
import win32con
import time

def mouse_scroll(delta):
    # delta는 스크롤 양을 나타냅니다. 양수는 위로 스크롤, 음수는 아래로 스크롤합니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)

# 스크롤할 양 정의 (-120 아래, +120 위)
scroll_amount = 120

# 스크롤 실행
time.sleep(2)
mouse_scroll(scroll_amount)