# native imports

from flask import Blueprint, jsonify, Response, request

# blueprint for module access
csrf : Blueprint = Blueprint('csrf', __name__)

@csrf.route("/get_csrf", methods=['GET'])
def get_csrf() -> Response :
    return jsonify(
        {
            "message" : 'Your csrf token has been attached to your cookie :D'
        }
    )