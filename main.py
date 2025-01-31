# native imports

from json import dumps
from sys import exit
from traceback import format_exc

# local imports
from fetcher_api.authorise import *
from fetcher_api.key import *

if __name__ == '__main__' :
    # probe the user for API credentials if there have been none provided before runtime
    makeKeyFile()

    # grab API information
    try :
        data_pair : dict = grabAPIInfo()
        client_id = data_pair['_id']
        client_secret = data_pair['_secret']
    except Exception as UnhandledException :
        print(format_exc())
        exit(-1)

    # attempt to load a token if one exists
    try :
        token = loadTokenData()
        validateToken(token['access_token'])
    except (TokenFileNotFoundError, TokenValidationError) :
        token = getAPIToken(client_id, client_secret)
    except Exception as UnhandledException:
        print(format_exc())
        exit(-1)

    try :
        url : str = 'https://api.myanimelist.net/v2/anime?offset=50&q=one&limit=50'
        response : Response = get(url, headers={'Authorization' : f'Bearer {token['access_token']}'})
        response.raise_for_status()
        data = response.json()
        response.close()
    except HTTPError :
        if response.status_code == 401 :
            token = refreshAPIToken(client_id, client_secret)
    print(dumps(data, indent=4))
    exit(1)