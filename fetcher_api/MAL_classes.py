from dataclasses import dataclass
from datetime import datetime
from json import loads
from requests import get, Response, HTTPError
from termcolor import colored
from typing import Any
from traceback import format_exc
from urllib.parse import quote

from fetcher_api.constants import *

class InvalidAnimeListQError(Exception) :
    """
    InvalidAnimeListQError : The query string is empty or invalid. String must
    be of at least length of 1 byte.
    """
    def __init__(self) :
        self.message = colored("The query string must be of at least length 1 and valid for search", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListLimitRangeError(Exception) :
    """
    InvalidAnimeListLimitRangeError : The limit exceeded range expected for the
    query. Range is between 1-100.
    """
    def __init__(self) :
        self.message = colored("The limit range must be between 1-100", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListOffsetRangeError(Exception) :
    """
    InvalidAnimeListOffsetRangeError : The offset was not within the threshold
    range. Value mus not be negative.
    """
    def __init__(self) :
        self.message = colored("The offset range must not be negative", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListFieldError(Exception) :
    """
    InvalidAnimeListFieldError : The field(s) present within the query was not
    a valid field or was a duplicate of a default field.
    """
    def __init__(self, field_in_question : str) :
        self.message = colored(f"\'{field_in_question}\' field is not a valid field or already included", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

@dataclass(init=False)
class AnimeListNode :
    """
    A container for data represented by each node in an AnimeList query result.

    Arguments :
        node_raw -- A dictionary containing raw data for each node in the data
        field for a query result.

        fields_queried -- A list of strings that corispond to valid fields for
        AnimeList queries.
        
    Field Attributes :
        id -- Unique identifier for an anime {default : None}

        title -- The anime name {default : ''}

        main_picture -- A dictionary containing links to provided assets on the
        MAL website {default : None}

        alternative_titles -- A dictionary containing strings or a list of
        strings of different names the anime goes by {default : None}

        start_date -- The datetime the anime was aired {default : None}

        end_date -- The datetime the anime was finished airing {default : None}

        synopsis -- A synopsis of the anime {default : None}

        mean -- The mean score of the anime {default : None}

        rank -- The rank of the anime {default : None}

        popularity -- The popularity of the anime {default : None}

        num_list_users -- The number of users who have this work in their list
        {default : 0}

        num_scoring_users -- The number of users who have this work scored
        {default : 0}

        nsfw -- The rating of the content in the anime {default : None} :
            'white' -> This work is safe for work

            'gray'  -> This work may be not safe for work

            'black' -> This work is not safe for work

        genres -- An array of dictionaries containing anime genres and their
        id values associated with the type of genre {default : None}

        created_at -- The date the anime entry was created {default : None}

        updated_at -- The date the anime entry was last updated
        {default : None}

        media_type -- A string representing the type of media this anime is 
        {default : None} :
        
        status -- Airing status {default : None}

        num_episodes -- The total number of episodes of this series, if 
        unknown, it is 0 {default : 0}

        start_season -- A dictionary containing the year and season the anime
        began airing {default : None}

        broadcast -- Broadcast date

        source -- Original work {default : None} :

        average_episode_duration -- Average length of episode in seconds
        {default : None}

        rating -- The rating of the anime {default : None}

        studios -- An array of dictionary objects containing anime studios with
        their corisponding ids {default : None}
    """
    # parameters for initialization
    node_raw : dict[str, Any]
    fields_queried : list[str]

    # field attributes
    id                       : int | None = None
    title                    : str = ''
    main_picture             : dict[str, str | None] | None = None
    alternative_titles       : dict[str, list[str] | str | None] | None = None
    start_date               : str | None = None
    end_date                 : str | None = None
    synopsis                 : str | None = None
    mean                     : float | None = None
    rank                     : int | None = None
    popularity               : int | None = None
    num_list_users           : int = 0
    num_scoring_users        : int = 0
    nsfw                     : str | None = None
    genres                   : list[tuple[int, str]] | None = None
    created_at               : datetime | None = None
    updated_at               : datetime | None = None
    media_type               : str | None = None
    status                   : str | None = None
    num_episodes             : int = 0
    start_season             : dict[str, int | str] | None = None
    broadcast                : dict[str, str | None] | None = None
    source                   : str | None = None
    average_episode_duration : int | None = None
    rating                   : str | None = None
    studios                  : list[tuple[int, str]] | None = None

    def __init__(self,
                 node_raw : dict[str, Any],
                 fields_queried : list[str]) :
        object.__setattr__(self, 'node_raw', node_raw)
        object.__setattr__(self, 'fields_queried', fields_queried)

        self.__post_init__()
    
    def __post_init__(self) :
        # only add the fields aquired from the query
        for attr, data in self.node_raw.items() :
            if attr in self.fields_queried :         
                object.__setattr__(self, attr, data)

@dataclass(init=False, frozen=True)
class AnimeList :
    """
    A container for holding a list of data results from a query.

    Arguments :
        q -- The query string for searching through the database

        limit -- The amount of nodes matching closest to the query string
        {default : 100}

        offset -- The amount of nodes skipped in the query resultant
        {default : 0}

        fields -- The fields to be included among the query resultant for each
        AnimeListNode object. If the field is not present in this array, the
        default value for that attribute will be what is specified in the
        description. {default : []}

    Field Attributes :
        raw_data -- The return json object from the https GET response

        data -- An array containing the AnimeListNode objects
    
        paging -- A dictionary containing a 'next' and 'previous' pagings that
        are derivative of the limit and offset values.
        
    Raises:
        InvalidAnimeListQError : The query string is invalid or doesn't meet
        the minimum requirements

        InvalidAnimeListLimitRangeError: The limit not in range [1,100]

        InvalidAnimeListOffsetRangeError: The offset not >= 0

        InvalidAnimeListFieldError: The field was not included in available
        selections for the query

        QueryException: HTTPError extension for cases where raised response
        code not being 200
    """
    # parameters for initialization    
    q                        : str
    limit                    : int
    offset                   : int
    fields                   : list[str]

    # list attributes
    raw_data                 : dict[str, Any]
    data                     : list[AnimeListNode]
    paging                   : dict[str, str]

    def __init__(self,
                 access_token : str,
                 q : str,
                 limit : int = 100,
                 offset : int = 0,
                 optional_fields : list[str] = []
                 ) :
        
        if len(q) <= 0 :
            raise InvalidAnimeListQError()
        object.__setattr__(self, "q", q)

        try :
            if limit > 100 or limit <= 0 :
                raise InvalidAnimeListLimitRangeError()
            object.__setattr__(self, "limit", limit)
        except InvalidAnimeListLimitRangeError as error :
            print(error)
            print(colored('limit variable will be set back to default value (100)', NOTE))
            object.__setattr__(self, "limit", 100)

        try :
            if offset < 0 :
                raise InvalidAnimeListOffsetRangeError()
            object.__setattr__(self, "offset", offset)
        except InvalidAnimeListOffsetRangeError as error :
            print(error)
            print(colored('offset variable will be set back to default value (0)', NOTE))
            object.__setattr__(self, "offset", 0)

        fin_fields = ANIMELISTNODE_DEFAULT_FIELDS[:]
        for field in optional_fields :
            try :
                if field not in ANIMELISTNODE_OPTIONAL_FIELDS or field in ANIMELISTNODE_DEFAULT_FIELDS:
                    raise InvalidAnimeListFieldError(field)
                else :
                    fin_fields.append(field)
            except InvalidAnimeListFieldError as error :
                print(error)
                print(colored(f'field \'{field}\' will not be queried or ignored', NOTE))
        object.__setattr__(self, "fields", fin_fields)
        
        self.__post_init__(access_token)

    def __post_init__(self, access_token : str) :
        try :
            # setup and submit the query through MAL
            url : str = ''.join([
                MAL_ANIME_ENDPOINT,
                '?',
                f'q={quote(self.q)}',
                f'&limit={self.limit}',
                f'&offset={self.offset}',
                f'&fields={','.join(self.fields)}' if len(self.fields) > 0 else ''
            ])
            header = {'Authorization' : f'Bearer {access_token}'}
            response : Response = get(url, headers=header)
            object.__setattr__(self, 'raw_data', dict(response.json()))
            response.raise_for_status()
        except HTTPError as QueryException:
            if self.raw_data['message'] == 'invalid q' :
                raise InvalidAnimeListQError
            raise QueryException
        except Exception as UnhandledException :
            print(format_exc(0))

        # put the paging dictionary with the paging attribute
        object.__setattr__(self, 'paging', self.raw_data['paging'])

        # populate the data attribute
        data_array : list[AnimeListNode] = []
        for raw_node in self.raw_data['data'] :
            data_array.append(AnimeListNode(raw_node['node'], self.fields))
        object.__setattr__(self, 'data', data_array)

        def get_next_page() -> AnimeList | None :
            return 