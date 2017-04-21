from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import datetime
import os
from dateutil import parser
from time import sleep
from youtube_upload import video_upload
from multiprocessing import Process
import argparse

from slack import send_msg

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'gcal_credentials.json'
APPLICATION_NAME = 'CamPals scheduler'

def upload_to_youtube(filename, title, description):
  a = argparse.Namespace() #ikke ror
  a.auth_host_name='localhost' #ikke ror
  a.auth_host_port=[8080, 8090] #ikke ror
  a.category="22" #ikke ror
  a.description=description
  a.file=filename #filnavn og lokasjon
  a.keywords="test, nice"
  a.logging_level='ERROR' #ikke ror
  a.noauth_local_webserver=False #ikke ror
  a.privacyStatus='public' #ikke ror
  a.title=title  #tittel
  video_upload(a)

class GCalender():
    def __init__(self,name, start_event, newfile_event, filenameQueue):
        self.get_credentials()
        self.name = name
        self.start = start_event
        self.newfile = newfile_event
        self.fileQ = filenameQueue
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
                title = event['summary']
                try:
                    desc = event['description']
                except:
                    desc = ''
                    pass
                start_time = event['start'].get('dateTime')
                end_time = event['end'].get('dateTime')
                #start_time = parser.parse(events[0]['start']['dateTime']).isoformat().split('+')[0]
                #end_time = parser.parse(events[0]['end']['dateTime']).isoformat().split('+')[0]

            if(start_time <= now) and (end_time >= now):
                if not self.start.is_set():
                    send_msg(title +" has started: "+ start_time.split('T')[1].split('+')[0] + ' '+start_time.split('T')[0])
                    print("Event started")
                    self.newfile.set()
                    self.start.set()
            else:
                if self.start.is_set():
                    print("Event ended")
                    send_msg(title +" has ended " + end_time.split('T')[1].split('+')[0] + ' '+end_time.split('T')[0])
                    self.start.clear()
                    filename = self.fileQ.get()
                    title = title + ' ' + start_time.split('T')[0]
                    print(filename, title, desc)
                    Process(target=upload_to_youtube,args=(filename, title, desc)).start()

if __name__ == "__main__":
    g = GCalender("CamPal",0,0, 0)
    event = g.get_event()
    if(event):
        print(event['summary'])
        print(event['description'])
    send_msg("Calender test")
