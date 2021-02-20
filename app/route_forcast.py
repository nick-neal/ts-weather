from flask import request, abort, make_response, jsonify
import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout, SSLError
import logging
import base64
from datetime import datetime, timezone
from config.tsurls import DARK_SKIES_URL
from config.tsurls import WEATHERSTACK_URL
from config.tskeys import DARK_SKIES_API_KEY
from config.tskeys import WEATHERSTACK_API_KEY
from config.tsconfig import HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT

# initialize logger for app
logger = logging.getLogger(__name__)

def getData(lat,lon,trans_id):

    logger.debug(f'[trans_id: {trans_id}, lat: {lat}, lon: {lon}]')

    weather_data = callForcastAPI2(lat,lon,trans_id)

    return weather_data

def callForcastAPI2(lat,lon,trans_id):

    message = {"status":"EMPTY"}
    if lat != "" and lon != "":
        # find way to restrict US address lookup.
        # also, will need to add forecast_days adjustment for planned stops, extended drives,
        # future trips, etc...
        uri = f'/forecast?access_key={WEATHERSTACK_API_KEY}&query={lat},{lon}&forecast_days=3&hourly=1&interval=1'
        full_url = f'{WEATHERSTACK_URL}{uri}'
        service = "WEATHER STACK /forecast"
        logger.info(f'Calling {service} API [trans_id: {trans_id}]')
        response = ''

        try:
            response = requests.get(url=full_url, timeout=(HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT))
        except HTTPError as http_err:
            logger.error(f'HTTP error occured on {service} [trans_id: {trans_id}]: {http_err}')
            eres = jsonify(status="ERROR", error_code="HTTP_ERROR", error_message="There was an HTTP_ERROR on the server side.")
            abort(make_response(eres,500))
        except SSLError as ssl_err:
            logger.error(f'SSL error occured on {service} [trans_id: {trans_id}]: {ssl_err}')
            eres = jsonify(status="ERROR", error_code="SSL_ERROR", error_message="There was an SSL_ERROR on the server side.")
            abort(make_response(eres,500))
        except ConnectTimeout as ct:
            logger.error(f'Connection Timeout occured on {service} [trans_id: {trans_id}]: {ct}')
            eres = jsonify(status="ERROR", error_code="HTTP_CONNECT_TIMEOUT", error_message="The server was unable to make an HTTP connection.")
            abort(make_response(eres,500))
        except ReadTimeout as rt:
            logger.error(f'Read Timeout occured on {service} [trans_id: {trans_id}]: {rt}')
            eres = jsonify(status="ERROR", error_code="HTTP_READ_TIMEOUT", error_message="The server took too long to respond.")
            abort(make_response(eres,500))
        except Exception as err:
            logger.error(f'Error occured on {service} [trans_id: {trans_id}]: {err}')
            eres = jsonify(status="ERROR", error_code="UNKNOWN_ERROR", error_message="An unknown error occured on the server side.")
            abort(make_response(eres,500))
        else:
            if response.status_code == 200:
                jres = response.json()
                logger.info(f'[trans_id: {trans_id}, status: OK')
                message = parseJsonResponse2(lat,lon,jres)
                message['status'] = "OK"

        return message


def callForcastAPI(lat,lon,trans_id):

    message = {"status":"EMPTY"}
    if lat != "" and lon != "":
        # find way to restrict US address lookup.
        uri = f'/forecast/{DARK_SKIES_API_KEY}/{lat},{lon}?exclude=[currently,minutely,daily,flags]'
        full_url = f'{DARK_SKIES_URL}{uri}'
        service = "DARK SKIES /forcast"
        logger.info(f'Calling {service} API [trans_id: {trans_id}]')
        response = ''

        try:
            response = requests.get(url=full_url, timeout=(HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT))
        except HTTPError as http_err:
            logger.error(f'HTTP error occured on {service} [trans_id: {trans_id}]: {http_err}')
            eres = jsonify(status="ERROR", error_code="HTTP_ERROR", error_message="There was an HTTP_ERROR on the server side.")
            abort(make_response(eres,500))
        except SSLError as ssl_err:
            logger.error(f'SSL error occured on {service} [trans_id: {trans_id}]: {ssl_err}')
            eres = jsonify(status="ERROR", error_code="SSL_ERROR", error_message="There was an SSL_ERROR on the server side.")
            abort(make_response(eres,500))
        except ConnectTimeout as ct:
            logger.error(f'Connection Timeout occured on {service} [trans_id: {trans_id}]: {ct}')
            eres = jsonify(status="ERROR", error_code="HTTP_CONNECT_TIMEOUT", error_message="The server was unable to make an HTTP connection.")
            abort(make_response(eres,500))
        except ReadTimeout as rt:
            logger.error(f'Read Timeout occured on {service} [trans_id: {trans_id}]: {rt}')
            eres = jsonify(status="ERROR", error_code="HTTP_READ_TIMEOUT", error_message="The server took too long to respond.")
            abort(make_response(eres,500))
        except Exception as err:
            logger.error(f'Error occured on {service} [trans_id: {trans_id}]: {err}')
            eres = jsonify(status="ERROR", error_code="UNKNOWN_ERROR", error_message="An unknown error occured on the server side.")
            abort(make_response(eres,500))
        else:
            if response.status_code == 200:
                jres = response.json()
                logger.info(f'[trans_id: {trans_id}, status: OK')
                message = parseJsonResponse(jres)
                message['status'] = "OK"

        return message

def cache_location(lat,lon,jres): # Used to start building a location cache system
    return False

def parseJsonResponse2(lat,lon,jres):
    response = {}

    response['latitude'] = lat
    response['longitude'] = lon
    response['timezone'] = jres['location']['timezone_id']
    response['utc_offset'] = jres['location']['utc_offset']

    #things are about to get lean here
    response['weather_data'] = []

    # strip any weather data from before current time.
    current_time = int(datetime.now(tz=timezone.utc).timestamp())
    for day in jres['forecast']:
        print(day)
        if int(day['date_epoch']) < current_time and current_time < (int(day['date_epoch']) + 86400):
            for x in day['hourly']:
                if int(x['time']) >= convertObservationTime(jres['current']['observation_time']):
                    tmp = x
                    tmp['time'] = convertEpoch(int(day['date_epoch']), x['time'])
                    response['weather_data'].append(tmp)
                else:
                    continue
        else:
            for x in day['hourly']:
                tmp = x
                tmp['time'] = convertEpoch(int(day['date_epoch']), x['time'])
                response['weather_data'].append(tmp)

    return response

def convertEpoch(date_epoch, hour):
    if hour == '0':
        return date_epoch
    else:
        return date_epoch + ((int(hour) / 100) * 3600) # ((24 hour format time) / 100) * (number of sec in an hour)



def convertObservationTime(ot):
    hour = int(ot.split(' ')[0].split(':')[0])
    am = True if ot.split(' ')[1] == 'AM' else False

    if hour == 1:
        return 100 if am else 1300
    elif hour == 2:
        return 200 if am else 1400
    elif hour == 3:
        return 300 if am else 1500
    elif hour == 4:
        return 400 if am else 1600
    elif hour == 5:
        return 500 if am else 1700
    elif hour == 6:
        return 600 if am else 1800
    elif hour == 7:
        return 700 if am else 1900
    elif hour == 8:
        return 800 if am else 2000
    elif hour == 9:
        return 900 if am else 2100
    elif hour == 10:
        return 1000 if am else 2200
    elif hour == 11:
        return 1100 if am else 2300
    elif hour == 12:
        return 0 if am else 1200


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
