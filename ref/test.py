import win32api
import win32con
import time

# 쉬프트 키 코드
VK_SHIFT = 0x10

# 쉬프트 키를 누르는 함수
def press_shift_key():
    win32api.keybd_event(VK_SHIFT, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)

# 쉬프트 키를 뗴는 함수
def release_shift_key():
    win32api.keybd_event(VK_SHIFT, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)

try:
    while True:
        press_shift_key()  # 쉬프트 키 누르기
        print("on")
        time.sleep(1)      # 1초 대기
        release_shift_key()  # 쉬프트 키 뗄기
        print("off")
        time.sleep(1)      # 1초 대기
except KeyboardInterrupt:
    pass
