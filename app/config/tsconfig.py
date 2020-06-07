import os

### APP CONFIG ###

APP_NAME = "ts-weather"
APP_VERSION = "ALPHA 20.9.0"
if 'APP_ENV' in os.environ:
    APP_ENV = os.environ['APP_ENV']
else:
    APP_ENV = "DEV" # DEV, TEST, PROD
APP_HOST = '0.0.0.0'
APP_PORT = 4082
APP_DEBUG = True
HTTP_CONNECT_TIMEOUT = 1 # set how long before you should giveup on an http connection.
HTTP_READ_TIMEOUT = 3 # set how long before you should give up on reading a response from an http connection.
