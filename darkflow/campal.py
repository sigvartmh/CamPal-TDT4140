from net.build import TFNet
from tensorflow import flags
import cv2
import unittest

class objectTracker:
    def findPerson(self, detectedObject):
        if(detectedObject['label'] == 'person'):
            pt1 = (detectedObject['topleft']['x'],detectedObject['topleft']['y'])
            pt2 = (detectedObject['bottomright']['x'],detectedObject['bottomright']['y'])
            return (pt1, pt2)

tracker = objectTracker()

options = { "model": "cfg/yolo-voc.cfg", "load": "bin/yolo-voc.weights", "threshold": 0.1}
tfnet = TFNet(options)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    result = tfnet.return_predict(frame)
    for item in result:
        print(item)
        try:
            (pt1, pt2) = tracker.findPerson(item)
            cv2.rectangle(frame, pt1, pt2, (255,0,0), 2)
            cv2.rectangle(frame, (pt1[0]-1,pt1[1]-1), (pt1[0]+150,pt1[1]-30), (255,0,0), -1)
            cv2.putText(frame, item['label'] , (pt1[0]+2,pt1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
        except:
            print("NoneType")
    cv2.imshow('frame',frame)
    #print(result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()

