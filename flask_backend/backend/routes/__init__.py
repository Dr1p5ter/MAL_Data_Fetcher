# native imports

from flask import Flask

# module imports for use elsewhere

from .csrf import csrf
from .user import user
from .anime import anime


def register_routes(app : Flask) -> None :
    """
    register_routes (function)

    Registers the route blueprints from the routes module in an organized and
    scalable fasion.

    Parameters
    ----------
    app : Flask
        The Flask object holding the app information.
    """
    app.register_blueprint(csrf, url_prefix="/csrf")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(anime, url_prefix="/anime")
