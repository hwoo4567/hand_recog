import cv2
import numpy as np
import mediapipe as mp
import typing

FINGER_CLOSE_THRESHOLD = 0.1

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

class HandRecog:
    # frame: image(MatLike) read from cap.read()
    def __init__(self, frame):
        self.frame = frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if rgb_frame is not None:
            self.results = hands.process(rgb_frame)
        else:
            raise TypeError("카메라가 존재하지 않습니다.")
        
        self.hands: typing.NamedTuple = self.results.multi_hand_landmarks
        
    def handExists(self):
        if self.hands:
            return True
        return False

    def drawHandPoint(self):
        if self.hands:
            # 각 손에 대한 반복
            for handLms in self.hands:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = self.frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    # 지점마다 원을 그람
                    cv2.circle(self.frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    
                # 점마다 라인을 연결
                mp_draw.draw_landmarks(self.frame, handLms, mp_hands.HAND_CONNECTIONS)

        return self.frame
    
    # finger_n: 손가락 번호 (엄지: 1, 검지: 2 ...)
    def isFingerClose(self, finger_n):
        if self.results.multi_hand_world_landmarks:
            # 여러 손이 인식되면 그 중 하나만
            handLms = self.results.multi_hand_world_landmarks[0]
            
            fingers = handLms.landmark  # index 0 - 20
            
            # n번째 손가락 끝의 번호 : n * 4
            tip = fingers[int(finger_n * 4)]  # 검지 끝
            hand_center = fingers[0]
            
            d = dist(tip.x, tip.y, hand_center.x, hand_center.y)
            if d <= FINGER_CLOSE_THRESHOLD:
                return True
            else:
                return False
        
        return False
        
    def getPointFromIdx(self, idx: int) -> tuple[float, float]:
        if self.hands:
            # 여러 손이 인식되면 그 중 하나만
            handLms = self.hands[0]
            fingers = handLms.landmark  # index 0 - 20
            center = fingers[idx]
                        
            return center.x, center.y
        
        # 손이 없으면 항상 중간점
        return 0.5, 0.5
    
    def getCenter(self) -> tuple[float, float]:  # x, y 범위 0 ~ 1
        return self.getPointFromIdx(0)  # 손바닥
    
    def getForefinger(self) -> tuple[float, float]:
        return self.getPointFromIdx(8)  # 검지 손가락 끝

def closeHandModel():
    hands.close()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = HandRecog(frame).drawHandPoint()
        
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    closeHandModel()
    cap.release()
    cv2.destroyAllWindows()
