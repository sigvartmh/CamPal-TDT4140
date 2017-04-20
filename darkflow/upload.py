
import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

RETRIABLE_EXCEPTIONS = (
        httplib2.HttpLib2Error,
        IOError, httplib.NotConnected,
        httplib.IncompleteRead,
        httplib.ImproperConnectionState,
        httplib.CannotSendRequest,
        httplib.CannotSendHeader,
        httplib.ResponseNotReady,
        httplib.BadStatusLine
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
MAX_RETRIES = 10
httplib2.RETRIES = 1

class Youtube():
    def start():
        pass
    def queue():
        pass
    def isDone():
        pass
