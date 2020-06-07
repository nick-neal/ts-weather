from flask import request, abort, make_response, jsonify
import requests
from requests.exceptions import HTTPError, ConnectTimeout, ReadTimeout, SSLError
import logging
import base64
from config.tsurls import DARK_SKIES_URL
from config.tskeys import DARK_SKIES_API_KEY
from config.tsconfig import HTTP_CONNECT_TIMEOUT, HTTP_READ_TIMEOUT

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
