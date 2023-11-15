import cv2
import hand
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

cap: cv2.VideoCapture

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
            x, y = recog.getForefinger()
            screenX, screenY = pyautogui.size()
            
            pyautogui.moveTo(int(screenX * x), int(screenY * y))
        
        # TODO: 손떨림 방지 기능 만들기, 손가락 인식에 margin 넣기
        
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