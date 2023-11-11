import cv2
import mediapipe as mp

# BaseOptions = mp.tasks.BaseOptions
# HandLandmarker = mp.tasks.vision.HandLandmarker
# HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
# mp_drawing = mp.solutions.drawing_utils

# # Create a hand landmarker instance with the image mode:
# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path="D:\dev\model\hand_landmarker.task"),
#     running_mode=VisionRunningMode.IMAGE)

# mp_image = mp.Image.create_from_file("./hand/test.jpg")

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()