# OpenCV Webcam test

import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

ramp_frames = 30
for i in range(ramp_frames):
        temp = cap.read()

ret, frame = cap.read()

# define the alpha and beta
alpha = 1.5 # Contrast control
beta = 60 # Brightness control

# call convertScaleAbs function
adjusted = cv.convertScaleAbs(frame, alpha=alpha, beta=beta)
    
if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
else:    
    cv.imshow('frame', frame)
    while True:
        if cv.waitKey(1) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()


# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_AREA)
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) == ord('q'):
#         break

# cap.release()
# cv.destroyAllWindows()
