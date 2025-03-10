# native imports

from flask import Blueprint, jsonify, Response, request

# local imports

from ..extensions import db
from ..models.user import User
from ._helpers import insert_data_to_session

# blueprint for module access
users : Blueprint = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_users() -> Response :
    """
    get_users (function)

    A route to extend queries for accessing users in the postgresql database.

    Returns
    -------
    ~flask.Response
        A response object based on the flask module containing data for each
        user in the database.
    """
    users : list = User.query.all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])

@users.route('/create_user_profile', methods=['POST'])
def create_user() -> Response :
    """
    create_user (function)

    A route dedicated to making a users profile based on information passed
    down from the request data.

    Returns
    -------
    Response
        A response object notifying the frontend that the user has been created
        successfully or not. 
        
        If it was a success, the response will return a
        201 code. 
        
        If there was an error in generating the user based off an schema or
        constraint violation then return a 409 code. In addition to a 409 code,
        it will send the attributes in question in the response back as
        'attr_in_question'.

        If the database was unable to make a connection a 500 code.
    """
    # check to make sure that the request is json
    if not request.is_json:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    # add the new user information to an object
    new_user : User = User()
    for attr in new_user.to_dict().keys() :
        new_user.__setattr__(attr, request.get_json().get(attr, None))

    # insert the user into the users table
    return insert_data_to_session(db, new_user)