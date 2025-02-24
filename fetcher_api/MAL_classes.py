# native imports

from dataclasses import dataclass
from requests import get, Response, HTTPError
from typing import Any
from urllib.parse import quote

# local imports

from fetcher_api.constants import *
from fetcher_api.key import APIKey
from fetcher_api.MAL_exceptions import *

# dataclasses

@dataclass(init=False)
class AnimeDetails :
    """
    (class object)

    A container for data represented by each Anime entry in the MAL database.

    Parameters
    ----------
    anime_id : int
        This is the unique identifier for MAL when assigning anime series in
        their database.
    attributes : list[str], optional
        The attributes to be included among the query resultant for each
        AnimeDetails object. If the attribute is not present in this array,
        the default value for that attribute will be what is specified in the
        description.
        By default [].

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
    pictures : list
        A dictionary containing image URIs for this anime.
    background : str
        A section of text covering anime production information/awards.
    related_anime : list
        Anime series that show relationship between original art and format.
    related_manga : list
        Manga series that show relationship between original art and format.
    recommendations : list
        A summary of recommended anime for those who like this anime.
    statistics : dict
        A rundown of user activity about this anime.
    """
    # parameters for initialization    
    anime_id                 : int
    attributes               : list[str]

    # node attributes
    raw_node                 : dict[str, Any]

    def __init__(self,
                 anime_id : str,
                 attributes : list[str] = []
                 ) :
        
        if anime_id <= 0 : 
            raise InvalidAnimeDetailsAnimeIdError(anime_id)
        object.__setattr__(self, 'anime_id', anime_id)

        fin_attributes = ANIME_DEFAULT_ATTRIBUTES[:]
        for attribute in attributes :
            try :
                if attribute not in ANIMEDETAILSNODE_OPTIONAL_ATTRIBUTES or attribute in ANIME_DEFAULT_ATTRIBUTES:
                    raise InvalidAnimeDetailsAttributeError(attribute)
                else :
                    fin_attributes.append(attribute)
            except InvalidAnimeListAttributeError as error :
                print(error)
            finally :
                continue
        object.__setattr__(self, "attributes", fin_attributes)
        
        self.__post_init__()

    def __post_init__(self) :
        try :
            # setup and submit the query through MAL
            url : str = ''.join([
                MAL_ANIME_ENDPOINT,
                f'/{self.anime_id}'
                '?',
                f'fields={','.join(self.attributes)}' if len(self.attributes) > 0 else ''
            ])
            header = {'X-MAL-CLIENT-ID' : f'{APIKey().getKey()[0]}'}
            response : Response = get(url, headers=header)
            object.__setattr__(self, 'raw_node', dict(response.json()))
            response.raise_for_status()
        except HTTPError as QueryException:
            raise QueryException
        
        # only add the attributes aquired from the query
        for attribute in self.attributes :
            object.__setattr__(self, attribute, self.raw_node.get(attribute, None))

    def __getattribute__(self, attribute : str) :
        # go around the native attributes first
        x_list = [
            'raw_node', 'anime_id', 'attributes', '__class__', '__dict__',
            '__post_init__', 'get_attribute_dict', '__getattribute__'
        ]
        if attribute in x_list :
            return super().__getattribute__(attribute)
        
        # make a check if the attribute was queried
        if attribute not in self.attributes :
            raise AnimeDetailsGetAttributeError(attribute)
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
        for attr in self.attributes :
            attr_dict[attr] = self.__getattribute__(attr)
        return attr_dict

@dataclass(init=False)
class AnimeListNode :
    """
    (class object)

    A container for data represented by each node in an AnimeList query result.

    Parameters
    ----------
    raw_node : dict[str, Any]
        A dictionary containing raw data for each node in the data attribute for a
        query result.

    attributes : list[str]
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
    
    Raises
    ------
    AnimeListNodeAttributeError
        There was an attribute being accessed that was not within the object
        attributes.
    """
    # parameters for initialization
    raw_node : dict[str, Any]
    attributes : list[str]

    def __init__(self,
                 raw_node : dict[str, Any],
                 attributes : list[str]) :
        object.__setattr__(self, 'raw_node', raw_node)
        object.__setattr__(self, 'attributes', attributes)

        self.__post_init__()
    
    def __post_init__(self) :
        # only add the attributes aquired from the query
        for attribute in self.attributes :
            object.__setattr__(self, attribute, self.raw_node.get(attribute, None))

    def __getattribute__(self, attribute : str) :
        # go around the native attributes first
        x_list = [
            'raw_node', 'attributes', '__class__', '__dict__',
            '__post_init__', 'get_attribute_dict', '__getattribute__'
        ]
        if attribute in x_list :
            return super().__getattribute__(attribute)
        
        # make a check if the attribute was queried
        if attribute not in self.attributes :
            raise AnimeListNodeGetAttributeError(attribute)
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
        for attr in self.attributes :
            attr_dict[attr] = self.__getattribute__(attr)
        return attr_dict

@dataclass(init=False, frozen=True)
class AnimeList :
    """
    (class object)

    A container for holding a list of data results from a query.

    Parameters
    ----------
    q : str
        The query string for searching through the database.
    limit : int, optional
        The amount of nodes matching closest to the query string.
        By default 100.
    offset : int, optional
        The amount of nodes skipped in the query resultant.
        By default 0.
    attributes : list[str], optional
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
    HTTPError
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
                 q : str,
                 limit : int = 100,
                 offset : int = 0,
                 attributes : list[str] = []
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
            object.__setattr__(self, "limit", 100)

        try :
            if offset < 0 :
                raise InvalidAnimeListOffsetRangeError()
            object.__setattr__(self, "offset", offset)
        except InvalidAnimeListOffsetRangeError as error :
            print(error)
            object.__setattr__(self, "offset", 0)

        fin_attributes = ANIME_DEFAULT_ATTRIBUTES[:]
        for attribute in attributes :
            try :
                if attribute not in ANIMELISTNODE_OPTIONAL_ATTRIBUTES or attribute in ANIME_DEFAULT_ATTRIBUTES:
                    raise InvalidAnimeListAttributeError(attribute)
                else :
                    fin_attributes.append(attribute)
            except InvalidAnimeListAttributeError as error :
                print(error)
            finally :
                continue
        object.__setattr__(self, "attributes", fin_attributes)
        
        self.__post_init__()

    def __post_init__(self) :
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
            header = {'X-MAL-CLIENT-ID' : f'{APIKey().getKey()[0]}'}
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
