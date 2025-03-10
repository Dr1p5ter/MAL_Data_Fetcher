# native imports

from os import getenv, _exit

class Config :
    """
    (class object)

    This is a container to hold all the app configurations necessary for the
    Flask application.
    """
    def __init__(self) :
        self.SQLALCHEMY_DATABASE_URI : str | None = getenv("DATABASE_URL", None)
        self.SQLALCHEMY_TRACK_MODIFICATIONS : bool = True
        self.SECRET_KEY : str | None = getenv("SECRET_KEY", None)
