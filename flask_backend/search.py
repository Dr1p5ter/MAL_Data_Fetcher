# package imports

from flask import request, jsonify

# local imports

from .config import app

# scope imports

from fetcher_api.key import APIKey
from fetcher_api.MAL_classes import AnimeList
from fetcher_api.token import APIToken

@app.route("/search", methods=['GET'])
def get_search() :
    test_list = AnimeList(
        APIToken(APIKey().getKey()).getToken()['access_token'],
        "one piece",
        limit=50,
    )
    return jsonify(test_list.raw_data)