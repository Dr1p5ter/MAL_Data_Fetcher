# native imports

from bcrypt import gensalt, checkpw, hashpw
from datetime import datetime, timezone, timedelta
from os import getenv
from typing import Any
from sqlalchemy.orm import validates

# local imports

from .base import BaseModel, db

class User(BaseModel):
    """
    (class object)

    A model for keeping track of user data and maintaining login information.
    """
    __tablename__ : str = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(int(getenv("USER_USERNAME_MAX_LEN"))),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(int(getenv("USER_PASSWORD_MAX_LEN"))),
        nullable=False
    )
    email = db.Column(
        db.String(int(getenv("USER_EMAIL_MAX_LEN"))), unique=True,
        nullable=False
    )
    fname = db.Column(
        db.String(int(getenv("USER_FNAME_MAX_LEN"))),
        nullable=True
    )
    m1name = db.Column(
        db.String(int(getenv("USER_M1NAME_MAX_LEN"))),
        nullable=True
    )
    m2name = db.Column(
        db.String(int(getenv("USER_M2NAME_MAX_LEN"))),
        nullable=True
    )
    lname = db.Column(
        db.String(int(getenv("USER_LNAME_MAX_LEN"))),
        nullable=True
    )
    nname = db.Column(
        db.String(int(getenv("USER_NNAME_MAX_LEN"))),
        nullable=True
    )
    bio = db.Column(
        db.String(int(getenv("USER_BIO_MAX_LEN"))),
        nullable=True
    )
    country = db.Column(
        db.String(int(getenv("USER_COUNTRY_MAX_LEN"))),
        nullable=True
    )
    state_province = db.Column(
        db.String(int(getenv("USER_STATE_PROVINCE_MAX_LEN"))),
        nullable=True
    )
    rec_question = db.Column(
        db.String(int(getenv("USER_REC_QUESTION_MAX_LEN"))),
        nullable=True
    )
    rec_answer = db.Column(
        db.String(int(getenv("USER_REC_ANSWER_MAX_LEN"))),
        nullable=True
    )
    date_of_birth = db.Column(
        db.DateTime(),
        nullable=True
    )
    usercreated = db.Column(
        db.DateTime(),
        default=datetime.now(timezone.utc),
        nullable=False
    )
    userinfochanged = db.Column(
        db.DateTime(), 
        default=datetime.now(timezone.utc),
        nullable=False,
        onupdate=datetime.now(timezone.utc)
    )
    passexpired = db.Column(
        db.DateTime(),
        default=(datetime.now(timezone.utc) + timedelta(days=90)),
        nullable=True,
    )
    lastlogin = db.Column(
        db.DateTime(),
        nullable=True
    )

    def __init__(self, request_json : Any) :
        for attr in self.__table__.columns.keys() :
            self.__setattr__(attr, request_json.get(attr, None))

    def __repr__(self) -> str :
        return f'<User {self.username}>'
    
    def to_dict(self) -> dict :
        """
        to_dict (public method)

        This is a helper method for returning dictionary objects.

        Returns
        -------
        dict
            json-like object
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
    def check_password(password : str, hashed_password : bytes) -> bool :
        """
        check_password (static method)

        This confirms a match with the hash provided in the database with the
        user provided string.

        Parameters
        ----------
        password : str
            Password in question to be checked against the database.
        hashed_password : bytes
            The hash that was present with the database.

        Returns
        -------
        bool
            True if they match, else False.
        """
        return checkpw(password.encode(), hashed_password)

    def _hash_password(password : str) -> bytes :
        """
        _hash_password (private method)

        This function hashes the a password.

        Parameters
        ----------
        password : str
            The password as a string.

        Returns
        -------
        bytes
            The hashed value in bytes.
        """
        return hashpw(password.encode(), gensalt())
    
    @validates('password')
    def _validates_password(self, key, password) :
        """
        validates_password (private method)

        This handles any instance of an insert or update event involving the
        password to ensure it is always hashed before storing into the
        database.

        Parameters
        ----------
        password : str
            Password mapped to this model.

        Returns
        -------
        bytes
            Hashed instance of the password.
        """
        return User._hash_password(password)
