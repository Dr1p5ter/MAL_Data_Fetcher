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
    # pprint(token)

    # example query
    animelist = AnimeList(token.getToken()['access_token'],
                          'Neon',
                          limit=1,
                          optional_fields=ANIMELISTNODE_OPTIONAL_FIELDS)

    for node in animelist.data :
        pprint(node)
    # pprint(animelist.paging)

    exit(1)