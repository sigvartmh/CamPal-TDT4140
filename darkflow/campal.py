from net.build import TFNet
from tensorflow import flags

import cv2
import cProfile, pstats, io
import threading, queue

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'gcal.json'
APPLICATION_NAME = 'CamPals scheduler'

trackerQueue = queue.Queue(1)
resultQueue = queue.Queue(1)
tfFrame = queue.Queue()
#fourcc = cv2.VideoWriter_fourcc('P', 'I', 'M', '1')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

#out = cv2.VideoWriter('test.avi', fourcc, 20.0, (int(cap.get(WIDTH)), int(cap.get(HEIGHT))))
ratio = 4
#options = { "model": "cfg/tiny-yolo-voc.cfg", "load": "bin/tiny-yolo-voc.weights", "threshold": 0.5, "gpu": 1.0}
options = { "model": "cfg/yolo-voc.cfg", "load": "bin/yolo-voc.weights", "threshold": 0.5, "gpu": 1.0}

class GCalender(object):
    def __init__(self):
        get_credentials()
    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(crendetial_dir)
        credential_path = os.path.join(credential_dir, 'gcal_credentials.json')
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
        self.credentials=credentials

    def get_gcal_service(self):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def get_events(self):
        service = self.get_gcal_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        eventResult = service.events.list(calendarId='primary', timeMin=now, maxResults=12, singleEvents=True, orderBy='startTime').execute()
        return eventsResult.get('items', [])

class ObjectTracker(threading.Thread):
    def run(self):
        self.setup()
        while True:
            frame = trackerQueue.get()
            tfframe = cv2.resize(frame, (0,0), fx=1/ratio, fy=1/ratio)
            print(tfframe.shape)
            result = self.tfnet.return_predict(tfframe)
            resultQueue.put(result)
            tfFrame.put(tfframe)
    def setup(self):
        self.tfnet = TFNet(options)

class VideoCapture():
    def run(self):
        self.setup()
        while True:
            ret, frame = self.cap.read()
            if(trackerQueue.empty()):
                trackerQueue.put_nowait(frame)
            elif(trackerQueue.full()):
                trackerQueue.get_nowait()
            if(resultQueue.full()):
                self.results = resultQueue.get()
            if(self.results):
                for item in self.results:
                    try:
                        (pt1, pt2) = self.findPerson(item)
                        #print("{0} and {1}".format(pt1,pt2))
                        cv2.rectangle(frame, pt1, pt2, (255,0,0), 2)
                        cv2.rectangle(frame, (pt1[0]-1,pt1[1]-1), (pt1[0]+150,pt1[1]-30), (255,0,0), -1)
                        cv2.putText(frame, item['label'] , (pt1[0]+2,pt1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
                        pos = int((((pt1[0]+pt2[0])/2)/MAX_WIDTH)*180)
                    except:
                        pass
            cv2.imshow('frame',frame)
            if not tfFrame.empty():
                tfframe = tfFrame.get()
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

    def findPerson(self, detectedObject):
        if(detectedObject['label'] == 'person'):
            pt1 = (detectedObject['topleft']['x']*ratio,detectedObject['topleft']['y']*ratio)
            pt2 = (detectedObject['bottomright']['x']*ratio,detectedObject['bottomright']['y']*ratio)
            return (pt1, pt2)

if __name__ == '__main__':

    ObjectTracker().start()
    VideoCapture().run()

