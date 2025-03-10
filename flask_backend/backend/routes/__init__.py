# native imports

from flask import Flask

# module imports for use elsewhere

from .csrf import csrf
from .hello import hello
from .users import users


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
    app.register_blueprint(hello, url_prefix="/hello")
    app.register_blueprint(users, url_prefix="/users")
