import numpy as np
import sys
sys.path.append('/usr/local/Cellar/opencv3/3.2.0/lib/python2.7/site-packages')
from imutils.object_detection import non_max_suppression
import imutils
import cv2
import time

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

camera = cv2.VideoCapture(0)
counter = 0
while True:
    start = time.time()
    (grabbed, frame) = camera.read()
    if not grabbed:
        break
    frame = imutils.resize(frame, width=800)
    orig = frame.copy()

    cv2.putText(frame, "CamPal Test", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
    if(counter):
        (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),padding=(8, 8), scale=1.05)
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    end = time.time()
    cv2.putText(frame, "counter:{} ".format(1/(end-start)),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Frame", frame)
    cv2.imshow("Original", orig)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    if key == ord("q"):
         break
camera.release()
cv2.destroyAllWindows()
