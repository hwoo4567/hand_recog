import cv2
import hand
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

cap: cv2.VideoCapture
cam_margin = 0.15

def posInMargin(x):
    if x < cam_margin:
        return 0.0
    elif x > 1- cam_margin:
        return 1.0
    else:
        return (x - 0.1) / (1 - cam_margin * 2)

def startCam():
    """ width, height"""
    global cap
    
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    return int(width), int(height)
    
def getFrame():
    ret, frame = cap.read()
    
    if ret:
        recog = hand.HandRecog(cv2.flip(frame, 1))
        recog_image = recog.drawHandPoint()
        
        if recog.handExists():
            cam_x, cam_y = recog.getForefinger()
            screen_x, screen_y = pyautogui.size()
            x, y = posInMargin(cam_x), posInMargin(cam_y)
            
            pyautogui.moveTo(int(screen_x * x), int(screen_y * y))
        
        # TODO: 손떨림 방지 기능 만들기
        
        img = cv2.cvtColor(recog_image, cv2.COLOR_BGR2RGB)
        
        
        return img
    else:
        return None

def closeCam():
    global cap
    
    cap.release()
    del cap
    print("Cam off")
    
    hand.closeHandModel()  #* must close the model