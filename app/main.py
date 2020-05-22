import connexion
import os
from logging.config import fileConfig
from config.tsconfig import *

# create application instance
app = connexion.App(__name__, specification_dir="./")

fileConfig('logging.cfg')

# create app config for /ts-main
app.add_api('swagger.yml')

# create a URL route for /
@app.route('/')
def home():
    """
        This functio responds to localhost:4080/
    """

    json_str = {"app_name":APP_NAME,"app_version":APP_VERSION,"app_env":APP_ENV}
    return json_str

# if running in standalone mode
if __name__ == '__main__':
    app.run(host=APP_HOST,port=APP_PORT,debug=APP_DEBUG)
