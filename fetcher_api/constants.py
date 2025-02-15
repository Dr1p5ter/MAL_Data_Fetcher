# Networking constants

MAL_OAUTH2_BASE : str = 'https://myanimelist.net'
MAL_OAUTH2_ENDPOINT : str = MAL_OAUTH2_BASE + '/v1/oauth2'
MAL_BASE : str = 'https://api.myanimelist.net'
MAL_ANIME_ENDPOINT : str = MAL_BASE + '/v2/anime'
MAL_MANGA_ENDPOINT : str = MAL_BASE + '/v2/manga'

# Organization constants

METADATA_PATH : str = '_api/'
TOKEN_PATH : str = METADATA_PATH + 'token.json'
KEY_PATH : str = METADATA_PATH + 'key.json'

# Exception printing color constants

DANGER = 'red'
WARNING = 'yellow'
NOTE = 'green'

# Key constants

API_CLIENT_ID_LEN : int = 32
API_CLIENT_SECRET_LEN : int = 64

# MAL_classes constants
ANIMELISTNODE_DEFAULT_ATTRIBUTES = [
    'id', 'title', 'main_picture'
]
ANIMELISTNODE_OPTIONAL_ATTRIBUTES = [
    'alternative_titles', 'start_date', 'end_date', 'synopsis', 'mean', 'rank',
    'popularity', 'num_list_users', 'num_scoring_users', 'nsfw', 'genres',
    'created_at', 'updated_at', 'media_type', 'status', 'num_episodes', 
    'start_season', 'broadcast', 'source', 'average_episode_duration',
    'rating', 'studios'
]

ANIMELISTNODE_ATTRIBUTES = ANIMELISTNODE_DEFAULT_ATTRIBUTES + ANIMELISTNODE_OPTIONAL_ATTRIBUTES