import connexion
import os
from logging.config import fileConfig

# Set app info
APP_NAME = "ts-weather"
APP_VERSION = "ALPHA 19.11.0"
APP_HOST = '0.0.0.0'
APP_PORT = 4082
APP_DEBUG = True

# create application instance
app = connexion.App(__name__, specification_dir="./")

fileConfig('logging.cfg')

'''
# Check env var tp find app level
TS_ENV = os.environ.get('TS_ENV_VAR')
if TS_ENV == "DEV":
    app.config.from_object('config.DevConfig')
elif TS_ENV == "TEST":
    app.config.from_object('config.TestConfig')
elif TS_ENV == "PROD":
    app.config.from_object('config.ProdConfig')
else:
    # treat like DEV
    app.config.from_object('Config.DevConfig')
'''

# create app config for /ts-main
app.add_api('swagger.yml')

# create a URL route for /
@app.route('/')
def home():
    """
        This functio responds to localhost:4080/
    """

    json_str = {"app_name":APP_NAME,"app_version":APP_VERSION}
    return json_str

# if running in standalone mode
if __name__ == '__main__':
    app.run(host=APP_HOST,port=APP_PORT,debug=APP_DEBUG)
