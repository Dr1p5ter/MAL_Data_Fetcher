# package imports

from flask import request, jsonify, redirect
from pprint import pprint
from traceback import format_exc

# local imports

from .config import app
from .uri_search import *

# home route

@app.route("/", methods=['GET'])
def get_home() :
    return redirect('/search')

APP_HOST : str = "localhost"
APP_PORT : int = 10001
if __name__ == '__main__' :
    # run the app on port 9000
    app.run(
        host=APP_HOST,
        port=APP_PORT
    )
