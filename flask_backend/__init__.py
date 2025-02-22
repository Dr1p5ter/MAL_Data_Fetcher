# package imports

from pprint import pprint
from traceback import format_exc

# scope imports

from fetcher_api.key import APIKey
from fetcher_api.token import APIToken

# probe the user for API credentials if there have been none provided before runtime
# and attempt to load a token if one exists
try :
    APIToken(APIKey().getKey())
except :
    pprint(format_exc())
    exit(-1)