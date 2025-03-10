# native import

from flask import Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from re import search as rsearch
from sqlalchemy.exc import (
    IntegrityError,
    InvalidRequestError,
    StatementError,
    DataError,
    OperationalError
)

def insert_data_to_session(db : SQLAlchemy, data : object) -> Response :
    """
    insert_data_to_session (function)

    This is a helper function to maintain PostgreSQL insertions into the database.

    Parameters
    ----------
    db : SQLAlchemy
        The flask database
    data : object
        A class that can be json serializable.

    Returns
    -------
    Response
        A return response for the frontend. Please see routes/users.py file for
        create_user().
    """
    # insert the data into the its respective table table
    try :
        # add entry to the session
        db.session.add(data)

        # commit changes to the session
        db.session.commit()

        # return success
        return jsonify ({
            'message' : 'User created'
        }), 201
    except (IntegrityError, StatementError, DataError) as err :
        # rollback the session
        db.session.rollback()

        # violations in accordance to pyycog2 errors
        msg = None
        attr_in_question = None
        if str(err.orig).find('UniqueViolation') >= 0 :
            # try to get the attr_in_question
            try :
                attr_in_question = rsearch(r'Key \((.*?)\)', str(err.orig)).group(1)
            except :
                attr_in_question = 'ERROR'
            
            msg = "Integrity constraint error caused by unique constraint"
        elif str(err.orig).find('NotNullViolation') >= 0 :
            # try to get the attr_in_question
            try :
                attr_in_question = rsearch(r'null value in column \"(.*?)\"', str(err.orig)).group(1)
            except :
                attr_in_question = 'ERROR'

            msg = "Integrity constraint error caused by not-null constraint"
        elif str(err.orig).find('ForeignKeyViolation') >= 0 :
            # try to get the attr_in_question
            try :
                attr_in_question = rsearch(r'Key \((.*?)\)', str(err.orig)).group(1)
            except :
                attr_in_question = 'ERROR'

            msg = "Integrity constraint error caused by foreign key constraint"
        elif str(err.orig).find('CheckViolation') >= 0 :
            # try to get the attr_in_question
            try :
                attr_in_question = rsearch(r'value for the column \"(.*?)\"', str(err.orig)).group(1)
            except :
                attr_in_question = 'ERROR'

            msg = "Integrity constraint error caused by check constraint"
        elif str(err.orig).find('ExclusionViolation') >= 0 :
            # try to get the attr_in_question
            try :
                attr_in_question = rsearch(r'Key \((.*?)\)', str(err.orig)).group(1)
                if attr_in_question.find(', ') >= 0 :
                    attr_in_question = attr_in_question.split(', ')
            except :
                attr_in_question = 'ERROR'

            msg = "Integrity constraint error caused by exclusion constraint"
        elif str(err.orig).find('InvalidTextRepresentation') >= 0 :
            # attr is not provided so this must be a forum error
            attr_in_question = 'ERROR'
            msg = "Integrity constraint error caused by Invalid or incomplete data type conversion"
        else :
            attr_in_question = 'ERROR'
            msg = "An unhandled exception occured please check details."
        
        # send out a response for the frontend
        return jsonify(
            {
                'message' : msg,
                'details' : str(err.orig)
            }
        ), 409
    except (InvalidRequestError, OperationalError) as err :
        # send out a response for the frontend
        return jsonify(
            {
                'message' : "An unhandled exception occured please check details.",
                'details' : str(err.orig)
            }
        ), 500
