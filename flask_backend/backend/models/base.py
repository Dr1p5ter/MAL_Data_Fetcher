# local imports

from backend.extensions import db

class BaseModel(db.Model) :
    """
    (class object)

    A super model for all other data models used in postgresql.
    """
    __abstract__ : str = True
    __tablename__ : str