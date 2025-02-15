# native imports

from dataclasses import dataclass
from datetime import datetime
from json import loads
from requests import get, Response, HTTPError
from termcolor import colored
from typing import Any
from traceback import format_exc
from urllib.parse import quote

# local imports

from fetcher_api.constants import *

class AnimeListNodeAttributeError(Exception) :
    """
    AnimeListNodeAttributeError _summary_

    The attribute being accessed was not queried for this object.
    
    Parameters
    ----------
    attr : str
        attribute not within the queried list
    """
    def __init__(self, attr : str) :
        self.message = colored(f"{attr} was not in attributes_queried upon calling getattr", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

@dataclass(init=False)
class AnimeListNode :
    """
    (class object)

    A container for data represented by each node in an AnimeList query result.

    Parameters
    ----------
    node_raw : dict[str, Any]
        A dictionary containing raw data for each node in the data attribute for a
        query result.

    attributes_queried : list[str]
        A list of strings that corispond to valid attributes for AnimeList queries.

    Attributes
    ----------
    id : int
        Unique identifier for an anime.
    title : str
        The anime name.
    main_picture : dict
        A dictionary containing links to provided assets on the MAL
        website.
    alternative_titles : dict
        A dictionary containing strings or a list of strings of different
        names the anime goes by.
    start_date : str
        The datetime the anime was aired.
    end_date : str
        The datetime the anime was finished airing.
    synopsis : str
        A synopsis of the anime.
    mean : float
        The mean score of the anime.
    rank : int
        The rank of the anime.
    popularity : int
        The popularity of the anime.
    num_list_users : int
        The number of users who have this work in their list.
    num_scoring_users : int
        The number of users who have this work scored.
    nsfw : str
        The rating of the content in the anime.
    genres : list
        An array of dictionaries containing anime genres and their id values
        associated with the type of genre.
    created_at : str
        The date the anime entry was created.
    updated_at : str
        The date the anime entry was last updated.
    media_type : str
        A string representing the type of media this anime is.
    status : str
        Airing status.
    num_episodes : int
        The total number of episodes of this series.
    start_season : dict
        A dictionary containing the year and season the anime began airing.
    broadcast : dict
        Broadcast date.
    source : str
        Original work.
    average_episode_duration : int
        Average length of episode in seconds.
    rating : str
        The rating of the anime.
    studios : list
        An array of dictionary objects containing anime studios with their
        corisponding ids.
    """
    # parameters for initialization
    node_raw : dict[str, Any]
    attributes_queried : list[str]

    def __init__(self,
                 node_raw : dict[str, Any],
                 attributes_queried : list[str]) :
        object.__setattr__(self, 'node_raw', node_raw)
        object.__setattr__(self, 'attributes_queried', attributes_queried)

        self.__post_init__()
    
    def __post_init__(self) :
        # only add the attributes aquired from the query
        for attribute in self.attributes_queried :
            object.__setattr__(self, attribute, self.node_raw.get(attribute, None))

    def __getattribute__(self, attribute : str) :
        # go around the native attributes first
        x_list = [
            'node_raw', 'attributes_queried', '__class__', '__dict__',
            '__post_init__', 'get_attribute_dict', '__getattribute__'
        ]
        if attribute in x_list :
            return super().__getattribute__(attribute)
        
        # make a check if the attribute was queried
        if attribute not in self.attributes_queried :
            raise AnimeListNodeAttributeError(attribute)
        return super().__getattribute__(attribute)
    def get_attribute_dict(self) -> dict :
        """
        get_attribute_dict (public method)

        Helper for returning only attributes that were queried.

        Returns
        -------
        dict
            A dictionary object containing only attributes grabbed from query.
        """
        attr_dict = dict()
        for attr in self.attributes_queried :
            attr_dict[attr] = self.__getattribute__(attr)
        return attr_dict

class InvalidAnimeListQError(Exception) :
    """
    InvalidAnimeListQError (exception)
    
    The query string is empty or invalid. String must be of at least length of
    one byte.
    """
    def __init__(self) :
        self.message = colored("The query string must be of at least length 1 and valid for search", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListLimitRangeError(Exception) :
    """
    InvalidAnimeListLimitRangeError
    
    The limit exceeded range expected for the query. Range is between 1-100.
    """
    def __init__(self) :
        self.message = colored("The limit range must be between 1-100", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListOffsetRangeError(Exception) :
    """
    InvalidAnimeListOffsetRangeError

    The offset was not within the threshold range. Value must not be negative.
    """
    def __init__(self) :
        self.message = colored("The offset range must not be negative", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListAttributeError(Exception) :
    """
    InvalidAnimeListAttributeError
    
    The attribute(s) present within the query was not a valid attribute or was a
    duplicate of a default attribute.
    """
    def __init__(self, attribute_in_question : str) :
        self.message = colored(f"\'{attribute_in_question}\' attribute is not a valid attribute or already included", WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

@dataclass(init=False, frozen=True)
class AnimeList :
    """
    (class object)

    A container for holding a list of data results from a query.

    Parameters
    ----------
    access_token : str
        The API access token.
    q : str
        The query string for searching through the database.
    limit : int, optional
        The amount of nodes matching closest to the query string.
        By default 100.
    offset : int, optional
        The amount of nodes skipped in the query resultant.
        By default 0.
    optional_attributes : list[str], optional
        The attributes to be included among the query resultant for each
        AnimeListNode object. If the attribute is not present in this array,
        the default value for that attribute will be what is specified in the
        description.
        By default [].
    
    Attributes
    ----------
    raw_data : dict[str, Any]
        The return json object from the https GET response.
    data : list[AnimeListNode]
        An array containing the AnimeListNode objects.
    paging : dict[str, str]
        A dictionary containing a 'next' and 'previous' pagings that are
        derivative of the limit and offset values.

    Raises
    ------
    InvalidAnimeListQError
        The query string is invalid or doesn't meet the minimum requirements.
    InvalidAnimeListLimitRangeError
        The limit not in range [1,100].
    InvalidAnimeListOffsetRangeError
        The offset not >= 0.
    InvalidAnimeListAttributeError
        The attribute was not included in available selections for the query.
    QueryException
        HTTPError extension for cases where raised response code not being 200.
    """
    # parameters for initialization    
    q                        : str
    limit                    : int
    offset                   : int
    attributes               : list[str]

    # list attributes
    raw_data                 : dict[str, Any]
    data                     : list[AnimeListNode]
    paging                   : dict[str, str]

    def __init__(self,
                 access_token : str,
                 q : str,
                 limit : int = 100,
                 offset : int = 0,
                 optional_attributes : list[str] = []
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

        fin_attributes = ANIMELISTNODE_DEFAULT_ATTRIBUTES[:]
        for attribute in optional_attributes :
            try :
                if attribute not in ANIMELISTNODE_OPTIONAL_ATTRIBUTES or attribute in ANIMELISTNODE_DEFAULT_ATTRIBUTES:
                    raise InvalidAnimeListAttributeError(attribute)
                else :
                    fin_attributes.append(attribute)
            except InvalidAnimeListAttributeError as error :
                print(error)
        object.__setattr__(self, "attributes", fin_attributes)
        
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
                f'&fields={','.join(self.attributes)}' if len(self.attributes) > 0 else ''
            ])
            header = {'Authorization' : f'Bearer {access_token}'}
            response : Response = get(url, headers=header)
            object.__setattr__(self, 'raw_data', dict(response.json()))
            response.raise_for_status()
        except HTTPError as QueryException:
            if self.raw_data['message'] == 'invalid q' :
                raise InvalidAnimeListQError
            raise QueryException

        # put the paging dictionary with the paging attribute
        object.__setattr__(self, 'paging', self.raw_data['paging'])

        # populate the data attribute
        data_array : list[AnimeListNode] = []
        for raw_node in self.raw_data['data'] :
            data_array.append(AnimeListNode(raw_node['node'], self.attributes))
        object.__setattr__(self, 'data', data_array)
