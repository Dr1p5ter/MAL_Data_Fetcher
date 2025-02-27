# package imports

from flask import request, jsonify

# local imports

from .config import app

# scope imports

from fetcher_api.MAL_classes import *

@app.route("/search", methods=['GET'])
def get_search() :
    test_details : AnimeDetails = AnimeDetails(
        40748,
        attributes=ANIMEDETAILSNODE_OPTIONAL_ATTRIBUTES[-4:] + ANIME_DEFAULT_ATTRIBUTES
    )
    return jsonify(test_details.raw_node)

@app.route("/testanimelistnode", methods=['GET'])
def get_animelistnode_test() :
    test_list : AnimeList = AnimeList('jujutsu kaisen')
    test_node : AnimeListNode = test_list.data[0]
    return jsonify(test_node.get_attribute_dict())