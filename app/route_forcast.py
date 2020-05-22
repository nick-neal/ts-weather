from flask import request
import requests
from requests.exceptions import HTTPError
import logging
import base64
from config.tsurls import DARK_SKIES_URL
from config.tskeys import DARK_SKIES_API_KEY

# initialize logger for app
logger = logging.getLogger(__name__)

def getData(lat,lon,trans_id):

    logger.debug(f'[trans_id: {trans_id}, lat: {lat}, lon: {lon}]')

    weather_data = callForcastAPI(lat,lon,trans_id)

    return weather_data

def callForcastAPI(lat,lon,trans_id):

    message = {"status":"EMPTY"}
    if lat != "" and lon != "":
        # find way to restrict US address lookup.
        uri = f'/forecast/{DARK_SKIES_API_KEY}/{lat},{lon}?exclude=[currently,minutely,daily,flags]'
        full_url = f'{DARK_SKIES_URL}{uri}'
        logger.info(f'Calling DARK SKIES /forcast API [trans_id: {trans_id}]')
        response = ''

        try:
            response = requests.get(full_url)

            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occured for [trans_id: {trans_id}]: {http_err}')
            message['status'] = "HTTP_ERROR"
        except Exception as err:
            logger.error(f'Error occured for [trans_id: {trans_id}]: {err}')
            message['status'] = "UNKNOWN_ERROR"
        else:
            if response.status_code == 200:
                jres = response.json()
                logger.info(f'[trans_id: {trans_id}, status: OK')
                message = parseJsonResponse(jres)
                message['status'] = "OK"

        return message

def parseJsonResponse(jres):
    response = {}

    response['latitude'] = jres['latitude']
    response['longitude'] = jres['longitude']
    response['timezone'] = jres['timezone']
    response['weather_data'] = jres['hourly']['data']
    if "alerts" in jres:
        response['alerts'] = jres["alerts"]
    else:
        response['alerts'] = "EMPTY"

    return response

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))
