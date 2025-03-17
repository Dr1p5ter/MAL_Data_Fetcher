# native imports

from flask import Blueprint, jsonify, Response, request

# local imports

from ..models.anime import Anime

from ._helpers import insert_data_to_session

# blueprint for module access
anime : Blueprint = Blueprint('anime', __name__)

@anime.route('/search/anime/<anime_id>', methods=['GET'])
def get_anime(anime_id : int) -> Response :
    """
    get_anime (function)

    A route to extend queries for accessing anime in the postgresql database.

    Parameters
    ----------
    anime_id : int
        The id of the anime to be queried.

    Returns
    -------
    ~flask.Response
        A response object based on the flask module containing data for the
        anime in the database.
    """
    # check to make sure that the request is json
    if not request.is_json:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    # add the new anime information to an object
    anime_data : Anime = Anime(anime_id, )