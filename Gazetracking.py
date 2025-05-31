import cv2
import dlib
import imutils
import numpy as np
import pyautogui as pag
import threading
from imutils import face_utils
from utils import *
from test import listen_and_execute  # Import speech command function

# Initialize face detector and predictor
shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Facial landmark indexes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Thresholds
EYE_AR_THRESH = 0.18
EYE_AR_CONSECUTIVE_FRAMES = 6
WINK_AR_DIFF_THRESH = 0.015
WINK_AR_CLOSE_THRESH = 0.18
WINK_CONSECUTIVE_FRAMES = 4
MOUTH_AR_THRESH = 0.4
MOUTH_AR_CONSECUTIVE_FRAMES = 5

# Counters
EYE_COUNTER = 0
WINK_COUNTER = 0
MOUTH_COUNTER = 0
INPUT_MODE = False
SCROLL_MODE = False
ANCHOR_POINT = (0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)

# Video capture
vid = cv2.VideoCapture(0)
resolution_w, resolution_h = 1366, 768
cam_w, cam_h = 640, 480
unit_w, unit_h = resolution_w / cam_w, resolution_h / cam_h

# Start speech recognition in a separate thread
def run_speech_commands():
    while True:
        listen_and_execute()

speech_thread = threading.Thread(target=run_speech_commands, daemon=True)
speech_thread.start()

# Main loop for gaze tracking
while True:
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=cam_w, height=cam_h)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray, 0)
    if len(rects) > 0:
        rect = rects[0]
    else:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        continue
    
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    mouth = shape[mStart:mEnd]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    nose = shape[nStart:nEnd]
    
    leftEye, rightEye = rightEye, leftEye
    mar = mouth_aspect_ratio(mouth)
    leftEAR, rightEAR = eye_aspect_ratio(leftEye), eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    diff_ear = np.abs(leftEAR - rightEAR)
    nose_point = (nose[3, 0], nose[3, 1])
    
    # Draw eye and mouth contours
    cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, YELLOW_COLOR, 1)
    cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, YELLOW_COLOR, 1)
    for (x, y) in np.concatenate((mouth, leftEye, rightEye), axis=0):
        cv2.circle(frame, (x, y), 2, GREEN_COLOR, -1)
    
    # Handle blinking, winking, and gaze movement
    if diff_ear > WINK_AR_DIFF_THRESH:
        if leftEAR < rightEAR and leftEAR < EYE_AR_THRESH:
            WINK_COUNTER += 1
            if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                pag.click(button='left')
                WINK_COUNTER = 0
        elif rightEAR < leftEAR and rightEAR < EYE_AR_THRESH:
            WINK_COUNTER += 1
            if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                pag.click(button='right')
                WINK_COUNTER = 0
        else:
            WINK_COUNTER = 0
    else:
        if ear <= EYE_AR_THRESH:
            EYE_COUNTER += 1
        else:
            EYE_COUNTER = 0
            WINK_COUNTER = 0

    if mar > MOUTH_AR_THRESH:
        MOUTH_COUNTER += 1
        if MOUTH_COUNTER >= MOUTH_AR_CONSECUTIVE_FRAMES:
            INPUT_MODE = not INPUT_MODE
            MOUTH_COUNTER = 0
            ANCHOR_POINT = nose_point
    else:
        MOUTH_COUNTER = 0
    
    if INPUT_MODE:
        cv2.putText(frame, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        x, y = ANCHOR_POINT
        nx, ny = nose_point
        w, h = 60, 35
        cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
        cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)
        
        dir = direction(nose_point, ANCHOR_POINT, w, h)
        cv2.putText(frame, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        drag = 18
        if dir == 'right':
            pag.moveRel(drag, 0)
        elif dir == 'left':
            pag.moveRel(-drag, 0)
        elif dir == 'up':
            pag.moveRel(0, -drag)
        elif dir == 'down':
            pag.moveRel(0, drag)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

vid.release()
cv2.destroyAllWindows()
