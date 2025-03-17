# native imports

from flask import Flask
from flask_wtf.csrf import generate_csrf
from os import getenv

# local imports

from .extensions import *

from config import Config

def create_app() -> Flask :
    """
    create_app (function)

    The flask app initialization function for linking configurations and db
    information. This is also a spot to plug in any extras from Flask or
    third-party providers.

    Returns
    -------
    Flask
        The flask application.
    """
    # Initialize the application
    app : Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config())

    # declare the db initialization
    db.init_app(app)
    from . import models

    # declare the migration initialization
    migrate.init_app(app, db)

    # configure CORS from extensions
    init_cors(app, f'http://{getenv("REACT_HOST")}:{getenv("REACT_PORT")}')

    # declare the CSRF initialization
    init_csrf(app)

    # make a CSRF handler
    @app.after_request
    def set_csrf_cookie(response) :
        csrf_token = generate_csrf()
        response.set_cookie('csrf_token', csrf_token)
        return response

    # begin to go through the registers in the register module
    from . import routes
    app.register_blueprint(routes.csrf)
    app.register_blueprint(routes.user)
    app.register_blueprint(routes.anime)

    # return the configured app
    return app
