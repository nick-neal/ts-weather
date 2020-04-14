from flask import request
import requests
from requests.exceptions import HTTPError
import logging
import base64

# initialize logger for app
logger = logging.getLogger(__name__)

# set constant vars
DARK_SKIES_URL = 'https://api.darksky.net'
# !!! SETUP IN CONFIG !!!
DARK_SKIES_API_KEY = '5561ed9c6a5ebbfbd4b04690f92e8c7e'


def getData():
    trans_id = request.form.get('trans_id')
    geo_list = base64ToString(request.form.get('geo_list'))
    return True

def callForcastAPI(lat,lon,trans_id):
    uri = f'/forecast/{DARK_SKIES_API_KEY}/{lat},{lon}?exclude=[currently,minutely,daily,flags]'
    return True

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
