from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import datetime
import os
from dateutil import parser
from time import sleep
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'gcal_credentials.json'
APPLICATION_NAME = 'CamPals scheduler'

class GCalender():
    def __init__(self,name, start_event, newfile_event):
        self.get_credentials()
        self.name = name
        self.start = start_event
        self.newfile = newfile_event
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
        eventsResult = service.events().list(calendarId=calId, timeMin=now, maxResults=12, singleEvents=True, orderBy='startTime', timeZone='Europe/Oslo').execute()
        return eventsResult.get('items', [])

    def get_event(self):
        service = self.get_gcal_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        calId = self.get_calendarId(self.name)
        eventsResult = service.events().list(calendarId=calId, timeMin=now, maxResults=1, singleEvents=True, orderBy='startTime', timeZone='Europe/Oslo').execute()
        event = eventsResult.get('items', [])
        if(event):
            return event[0]
        else:
            return None

    def get_calendarId(self, name):
        service = self.get_gcal_service()
        clist = service.calendarList().list().execute()
        for cal in clist['items']:
            if cal['summary'] == name:
                return cal['id']

    def start_calender_check(self):
        start_time = datetime.datetime(2017,1,1).isoformat()
        end_time = datetime.datetime(2017,1,1).isoformat()
        while True:

            #events = self.get_events()
            event = self.get_event()
            now = datetime.datetime.now().isoformat() #.split('.')[0]
            #if(events):
            if(event):
                #print(event)
                start_time = event['start'].get('dateTime')
                end_time = event['end'].get('dateTime')
                #start_time = parser.parse(events[0]['start']['dateTime']).isoformat().split('+')[0]
                #end_time = parser.parse(events[0]['end']['dateTime']).isoformat().split('+')[0]

            if(start_time <= now) and (end_time >= now):
                if not self.start.is_set():
                    print("Event started")
                    self.newfile.set()
                    self.start.set()
            else:
                if self.start.is_set():
                    print("Event ended")
                    self.start.clear()
if __name__ == "__main__":
    g = GCalender("CamPal",0,0)
    g.start_calender_check()
