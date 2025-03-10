# native imports

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# database for postgresql
db : SQLAlchemy = SQLAlchemy()

# migration handler for SQLAlchemy and Alembic
migrate : Migrate = Migrate()

# Cross origin resource sharing config
def init_cors(app : Flask, origin : list[str] | str) -> None :
    """
    init_cors (function)

    This function initializes CORS for the flask application. This is primarily
    used so that the backend can communicate with the frontend and vise-versa.

    Parameters
    ----------
    app : Flask
        The application being created.
    origin : list[str]
        The origins used for the application to limit external use.
    """
    CORS(
        app,
        resources={
            r'/*' : {
                'origins' : origin
            }
        },
        supports_credentials=True
    )

# Cross-site request forgery
def init_csrf(app : Flask) -> None :
    """
    init_csrf (function)

    This function initializes CSRF for the flask application. This is primarily
    used so that the frontend is not compromised.

    Parameters
    ----------
    app : Flask
        The application being created.
    """
    CSRFProtect(app)
