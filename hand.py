import cv2
import numpy as np
import mediapipe as mp

FINGER_CLOSE_THRESHOLD = 0.1

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def drawHandPoint(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        # 각 손에 대한 반복
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # 지점마다 원을 그람
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                
            # 점마다 라인을 연결
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    return frame

def getHandPoints(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    """
    HandLandmarkerResult:
    Handedness:
        Categories #0:
        index        : 0
        score        : 0.98396
        categoryName : Left
    Landmarks:                   multi_hand_landmarks
        Landmark #0:
        x            : 0.638852
        y            : 0.671197
        z            : -3.41E-7
        Landmark #1:
        x            : 0.634599
        y            : 0.536441
        z            : -0.06984
        ... (21 landmarks for a hand)
    WorldLandmarks:             multi_hand_world_landmarks
        Landmark #0:
        x            : 0.067485
        y            : 0.031084
        z            : 0.055223
        Landmark #1:
        x            : 0.063209
        y            : -0.00382
        z            : 0.020920
        ... (21 world landmarks for a hand)
    """
    
    return results

def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def fingerClose(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_world_landmarks:
        # 여러 손이 인식되면 그 중 하나만
        handLms = results.multi_hand_world_landmarks[0]
        
        fingers = handLms.landmark  # index 0 - 20
        tip = fingers[8]
        hand_center = fingers[0]
                    
        d = dist(tip.x, tip.y, hand_center.x, hand_center.y)
        if d <= FINGER_CLOSE_THRESHOLD:
            return True
        else:
            return False
    else:
        return False

def closeHandModel():
    hands.close()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = drawHandPoint(frame)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    closeHandModel()
    cap.release()
    cv2.destroyAllWindows()
