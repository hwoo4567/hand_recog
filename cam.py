import cv2
import hand
import control
import gesture as g

cap: cv2.VideoCapture
cam_margin = 0.2
recog_info = None

# global
mouse_pos = (0.0, 0.0)
hand_state = (0, 0, 0, 0)


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
    global mouse_pos, hand_state
    
    if recog_info is None:
        return
    
    if recog_info.handExists():
        screen_x, screen_y = control.get_screen_size()
        cam_x, cam_y = recog_info.getStandardPoint()
        x, y = posInMargin(cam_x), posInMargin(cam_y)
        mouse_pos = x, y
        
        control.moveTo(int(screen_x * x), int(screen_y * y))
        
        temp = recog_info.isFingerClose(2), recog_info.isFingerClose(3), recog_info.isFingerClose(4), recog_info.isFingerClose(5)
        gesture = tuple(int(not i) for i in temp)
        hand_state = gesture
        
        # tinkercad gesture
        if gesture == g.rotation_view:
            control.mouseDown("right")
        elif gesture == g.pan_view:
            control.mouseDown("middle")
        elif gesture == g.left_click:
            control.mouseDown("left")
        else:
            control.mouseUp("right")
            control.mouseUp("middle")
            control.mouseUp("left")

def getInfo():
    global mouse_pos, hand_state
    simpler = tuple(round(i, 3) for i in mouse_pos)
    
    return f"mouse_pos: {simpler}, hand_state: {hand_state}"

def closeCam():
    global cap
    
    cap.release()
    del cap
    print("Cam off")
    
    hand.closeHandModel()  #* must close the model