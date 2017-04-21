from net.build import TFNet
from tensorflow import flags
from calender import GCalender
import cv2
import cProfile, pstats, io
import queue
from multiprocessing import Process, Queue, RLock, Event
import datetime
from time import sleep
from servo import Servo
#flags.DEFINE_boolean("verbalise", False, "say out loud while building graph")
#flags.DEFINE_boolean("verbalise", True, "say out loud while building graph")

#fourcc = cv2.VideoWriter_fourcc('P', 'I', 'M', '1')
#fourcc = cv2.VideoWriter_fourcc(*'avc1')
#fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
print("fourcc:", fourcc)
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
                print("Taking camera frame")
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

class VideoCapture():
    def __init__(self, trackerQueue, resultQueue, tfFrame, recordingEvent, newfileEvent, fileQ, posQ):

        self.trackerQueue = trackerQueue
        self.resultQueue = resultQueue
        self.tfFrame = tfFrame

        self.fileQ = fileQ
        self.recording = recordingEvent
        self.newfile = newfileEvent

        self.posQ = posQ
        self.pos = 90
    def run(self):
        self.setup()
        StartLockState = False
        filename = 0
        target = 90
        self.posQ.put(target)
        while True:
            try:
                self.posQ.put_nowait(self.pos)
            except:
                pass
            self.recording.wait()
            if self.newfile.is_set():
                print("New file created")
                size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                videofile = cv2.VideoWriter()
                videofile.open('lecture_'+str(filename)+'.mkv',fourcc, 10, size)
                self.newfile.clear()
                filename += 1
            ret, frame = self.cap.read()
            if ret:
                videofile.write(frame)
            try:
                if ret:
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
                        target = int((((pt1[0]+pt2[0])/2)/self.MAX_WIDTH)*180)

                        #print("pos:", pos)
                    except:
                        print("something failed")
                        pass
            if(target > 110):
                self.pos += 0.2
                #self.servo.move(str(self.pos).encode('utf8'))
            elif(target < 70):
                self.pos -= 0.2
                #self.servo.move(str(self.pos).encode('utf8'))

            if ret:
                cv2.imshow('frame',frame)
            if not self.tfFrame.empty():
                tfframe = self.tfFrame.get()
                cv2.imshow('tfFrame',tfframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if not self.recording.is_set():
                videofile.release()
                self.fileQ.put('lecture_'+str(filename-1)+'.mkv')
                print("Closed file")


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
        if(detectedObject['label'] == 'person'):
            pt1 = (detectedObject['topleft']['x']*scale_ratio,detectedObject['topleft']['y']*scale_ratio)
            pt2 = (detectedObject['bottomright']['x']*scale_ratio,detectedObject['bottomright']['y']*scale_ratio)
            return (pt1, pt2)

if __name__ == '__main__':
    trackerQueue = Queue(1)
    resultQueue = Queue(1)
    posQ = Queue(1)
    fileQ=Queue(1)
    tfFrame = Queue()
    trackerReady = Event()
    startRecording = Event()
    newfile = Event()
    servo = Servo('/dev/tty.wchusbserial1420', posQ)
    g = GCalender("CamPal",startRecording, newfile, fileQ)

    calender=Process(target=g.start_calender_check)
    tracker=Process(target=ObjectTracker, args=(trackerQueue,resultQueue,tfFrame))
    servoProcess = Process(target=servo.run)

    calender.start()
    tracker.start()
    servoProcess.start()
    VideoCapture(trackerQueue,resultQueue,tfFrame, startRecording, newfile, fileQ, posQ).run()
