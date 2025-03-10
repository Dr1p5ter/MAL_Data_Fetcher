# native imports

from flask import Blueprint

# blueprint for module access
hello : Blueprint = Blueprint('hello', __name__)

@hello.route('/')
def index() -> str :
    """
    index (function)

    This route extends a hello world. This is primarily used for testing and
    nothing more.

    Returns
    -------
    str
        A 'hello world' prompt.
    """
    return "Hello, World!"
