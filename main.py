# native imports

from sys import exit
from traceback import format_exc
from pprint import pprint

# local imports
from fetcher_api.token import APIToken
from fetcher_api.key import APIKey
from fetcher_api.MAL_classes import *

if __name__ == '__main__' :
    # probe the user for API credentials if there have been none provided before runtime
    try :
        key : APIKey = APIKey()
    except :
        pprint(format_exc())
        exit(-1)
    # pprint(key)

    # attempt to load a token if one exists
    try :
        token : APIToken = APIToken(key.getKey())
    except :
        pprint(format_exc())
        exit(-1)

    # example query
    animelist = AnimeList(token.getToken()['access_token'],
                          'one',
                          limit=1,
                          optional_attributes=ANIMELISTNODE_ATTRIBUTES)

    animenodelist : list[AnimeListNode]= animelist.data
    for node in animenodelist :
        pprint(node.get_attribute_dict())

    exit(1)