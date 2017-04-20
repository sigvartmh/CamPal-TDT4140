from net.build import TFNet
from tensorflow import flags

import cv2
import cProfile, pstats, io
import queue
from multiprocessing import Process, Queue
import datetime

#flags.DEFINE_boolean("verbalise", False, "say out loud while building graph")
#flags.DEFINE_boolean("verbalise", True, "say out loud while building graph")

#fourcc = cv2.VideoWriter_fourcc('P', 'I', 'M', '1')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#out = cv2.VideoWriter('test.avi', fourcc, 20.0, (int(cap.get(WIDTH)), int(cap.get(HEIGHT))))
ratio = 4
#options = { "model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.5, "gpu": 1.0}
options = { "model": "./cfg/yolo-voc.cfg", "load": "./bin/yolo-voc.weights", "threshold": 0.5, "gpu": 1.0, "verbalise": False}

class ObjectTracker():#threading.Thread):
    def __init__(self, trackerQueue, resultQueue, tfFrame):
#        super(ObjectTracker, self).__init__()
        self.trackerQueue=trackerQueue
        self.resultQueue=resultQueue
        self.tfFrame=tfFrame
        self.run()

    def run(self):
        self.setup()
        try:
            while self.alive:
            #tfframe = self.trackerQueue.get()
                frame = self.trackerQueue.get()
                tfframe = cv2.resize(frame, (0,0), fx=1/ratio, fy=1/ratio)
            #print(tfframe.shape)
                result = self.tfnet.return_predict(tfframe)
                self.resultQueue.put(result)
                self.tfFrame.put(tfframe)
                if not self.alive:
                    return
        except:
            pass
    def setup(self):
        print(self.trackerQueue)
        self.alive = True
        self.tfnet = TFNet(options)

    def stop(self):
        self.alive = False
        #self.join()


class VideoCapture():
    def __init__(self, trackerQueue, resultQueue, tfFrame):
        self.trackerQueue = trackerQueue
        self.resultQueue = resultQueue
        self.tfFrame = tfFrame

    def run(self):
        self.setup()
        while True:
            ret, frame = self.cap.read()
            try:
                self.trackerQueue.put_nowait(frame)
            except:
                pass

            if(self.resultQueue.full()):
                self.results = self.resultQueue.get()
            if(self.results):
                for item in self.results:
                    try:
                        (pt1, pt2) = self.findPerson(item, ratio)
                        #print("{0} and {1}".format(pt1,pt2))
                        cv2.rectangle(frame, pt1, pt2, (255,0,0), 2)
                        cv2.rectangle(frame, (pt1[0]-1,pt1[1]-1), (pt1[0]+150,pt1[1]-30), (255,0,0), -1)
                        cv2.putText(frame, item['label'] , (pt1[0]+2,pt1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
                        pos = int((((pt1[0]+pt2[0])/2)/MAX_WIDTH)*180)
                    except:
                        pass
            cv2.imshow('frame',frame)
            if not self.tfFrame.empty():
                tfframe = self.tfFrame.get()
                cv2.imshow('tfFrame',tfframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        '''
                print("NoneType")
        '''
    def setup(self):
        WIDTH=3
        HEIGHT=4
        self.results = None
        self.cap = cv2.VideoCapture(0)
        self.MAX_WIDTH=self.cap.get(WIDTH)
        self.MAX_HEIGHT=self.cap.get(HEIGHT)

    def findPerson(self, detectedObject, scale_ratio):
        #if(detectedObject['label'] == 'person'):
            pt1 = (detectedObject['topleft']['x']*scale_ratio,detectedObject['topleft']['y']*scale_ratio)
            pt2 = (detectedObject['bottomright']['x']*scale_ratio,detectedObject['bottomright']['y']*scale_ratio)
            return (pt1, pt2)

if __name__ == '__main__':
    trackerQueue = Queue(1)
    resultQueue = Queue(1)
    tfFrame = Queue()

    tracker=Process(target=ObjectTracker, args=(trackerQueue,resultQueue,tfFrame))
    tracker.start()
    VideoCapture(trackerQueue,resultQueue,tfFrame).run()

