from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import datetime
import os
from dateutil import parser
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'gcal_credentials.json'
APPLICATION_NAME = 'CamPals scheduler'

class GCalender():
    def __init__(self,name, start, stop):
        self.get_credentials()
        self.name = name
        self.start = start
        self.stop = stop
    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gcal_credentials.json')
        store = Storage(credential_path)
        self.credentials = store.get()

        if not self.credentials or self.credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            self.credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)

    def get_gcal_service(self):
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        return service

    def get_events(self):
        service = self.get_gcal_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        calId = self.get_calendarId(self.name)
        eventsResult = service.events().list(calendarId=calId, timeMin=now, maxResults=12, singleEvents=True, orderBy='startTime').execute()
        return eventsResult.get('items', [])

    def get_calendarId(self, name):
        service = self.get_gcal_service()
        clist = service.calendarList().list().execute()
        for cal in clist['items']:
            if cal['summary'] == name:
                return cal['id']
    def start_calender_check(self):
        while True:
            events = self.get_events()
            if(events):
                now = datetime.datetime.now().isoformat().split('.')[0]
                starttime = parser.parse(events[0]['start']['dateTime']).isoformat().split('+')[0]
                endttime = parser.parse(events[0]['end']['dateTime']).isoformat().split('+')[0]
                if(starttime==now):
                    print("Event start")
                elif(endttime==now):
                    print("Event ended")

g = GCalender("CamPal",0,0)
g.start_calender_check()
