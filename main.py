from authorise import *
from json import dumps
from key import *
from sys import exit
from traceback import format_exc
from query import *

if __name__ == '__main__' :
    # probe the user for API credentials if there have been none provided before runtime
    makeKeyFile()

    # grab API information
    try :
        data_pair : tuple[str, str] = grabAPIInfo()
        client_id = data_pair[0]
        client_secret = data_pair[1]
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
        url : str = 'https://api.myanimelist.net/v2/anime/22429?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
        response : Response = get(url, headers={'Authorization' : f'Bearer {token['access_token']}'})
        response.raise_for_status()
        data = response.json()
        response.close()
    except HTTPError :
        if response.status_code == 401 :
            token = refreshAPIToken(client_id, client_secret)
    print(dumps(data, indent=4))
    exit(1)