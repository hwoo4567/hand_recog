import cv2
import pyautogui
import hand
import gesture as g
import os  # for log message

pyautogui.PAUSE = 0.0

cap: cv2.VideoCapture
cam_margin = 0.2
recog_info = None

def posInMargin(x):
    if x < cam_margin:
        return 0.0
    elif x > 1- cam_margin:
        return 1.0
    else:
        return (x - cam_margin) / (1 - cam_margin * 2)

def startCam():
    """ width, height"""
    global cap
    
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    return int(width), int(height)

def init():
    global recog_info
    ret, frame = cap.read()
    
    if ret:
        recog_info = hand.HandRecog(cv2.flip(cv2.flip(frame, 0), 1), stabilization=True)  # 상하, 좌우 반전
    else:
        recog_info = None
    
def getFrame(show_margin=False):
    if recog_info is None:
        return None
    
    recog_image = recog_info.drawHandPoint()
    img = cv2.cvtColor(recog_image, cv2.COLOR_BGR2RGB)
    
    if show_margin:
        h, w = img.shape[:2]
        start_point = int(w * cam_margin), int(h * cam_margin)
        end_point = w - start_point[0], h - start_point[1]
        
        img = cv2.rectangle(img, start_point, end_point, (0, 0, 0), 2)
    
    return img

def controlMouseByFrame():
    if recog_info is None:
        return
    
    if recog_info.handExists():
        cam_x, cam_y = recog_info.getStandardPoint()
        screen_x, screen_y = pyautogui.size()
        x, y = posInMargin(cam_x), posInMargin(cam_y)
        
        pyautogui.moveTo(int(screen_x * x), int(screen_y * y), duration=0.1)
        
        temp = recog_info.isFingerClose(2), recog_info.isFingerClose(3), recog_info.isFingerClose(4), recog_info.isFingerClose(5)
        gesture = tuple(int(not i) for i in temp)
                
        # tinkercad gesture
        if gesture == g.rotation_view:
            pyautogui.mouseDown(button="right")
        elif gesture == g.pan_view:
            pyautogui.mouseDown(button="middle")
        elif gesture == g.left_click:
            pyautogui.mouseDown(button="left")
        else:
            pyautogui.mouseUp(button="middle")
            pyautogui.mouseUp(button="left")
            pyautogui.mouseUp(button="right")
            
        os.system("cls")
        print(gesture)
        
def closeCam():
    global cap
    
    cap.release()
    del cap
    print("Cam off")
    
    hand.closeHandModel()  #* must close the model