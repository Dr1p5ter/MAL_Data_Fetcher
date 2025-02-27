# native imports

from termcolor import colored

# local imports

from fetcher_api.constants import WARNING, DANGER

# helpers

def danger(err_msg : str) -> str :
    return colored(f'DANGER : {err_msg}', DANGER)

def warning(err_msg : str) -> str :
    return colored(f'WARNING : {err_msg}', WARNING)

# exceptions

class AnimeDetailsGetAttributeError(Exception) :
    """
    AnimeDetailsGetAttributeError (exception)

    The attribute being accessed was not queried for this object.
    
    Parameters
    ----------
    attr : str
        attribute not within the queried list
    """
    def __init__(self, attr : str) :
        self.message = danger(f'{attr} was not in attributes upon calling getattr')
        super().__init__(self.message)
    
    def __str__(self) :
        return self.message

class AnimeListNodeGetAttributeError(Exception) :
    """
    AnimeListNodeGetAttributeError (exception)

    The attribute being accessed was not queried for this object.
    
    Parameters
    ----------
    attr : str
        attribute not within the queried list
    """
    def __init__(self, attr : str) :
        self.message = danger(f'{attr} was not in attributes upon calling getattr')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class AnimeListGetAttributeError(Exception) :
    """
    AnimeListGetAttributeError (exception)

    The attribute being accessed was not queried for this object.
    
    Parameters
    ----------
    attr : str
        attribute not within the queried list
    """
    def __init__(self, attr : str) :
        self.message = danger(f'{attr} was not in attributes upon calling getattr')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeDetailsAnimeIdError(Exception) :
    """
    InvalidAnimeDetailsAnimeIdError (exception)

    The anime id was not valid during initialization.
    
    Parameters
    ----------
    id : int
        id not within the valid bounds
    """
    def __init__(self, id : int) :
        self.message = warning(f'{id} was not within a valid range, must be posative')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeDetailsAttributeError(Exception) :
    """
    InvalidAnimeDetailsAttributeError
    
    The attribute(s) present within the query was not a valid attribute or was a
    duplicate of a default attribute.
    """
    def __init__(self, attribute_in_question : str) :
        self.message = warning(f'\'{attribute_in_question}\' attribute is not a valid attribute or already included')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListQError(Exception) :
    """
    InvalidAnimeListQError (exception)
    
    The query string is empty or invalid. String must be of at least length of
    one byte.
    """
    def __init__(self) :
        self.message = warning('The query string must be of at least length 1 and valid for search')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListLimitRangeError(Exception) :
    """
    InvalidAnimeListLimitRangeError
    
    The limit exceeded range expected for the query. Range is between 1-100.
    """
    def __init__(self) :
        self.message = warning('The limit range must be between 1-100')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidAnimeListOffsetRangeError(Exception) :
    """
    InvalidAnimeListOffsetRangeError

    The offset was not within the threshold range. Value must not be negative.
    """
    def __init__(self) :
        self.message = warning('The offset range must not be negative')
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
        self.message = warning(f'\'{attribute_in_question}\' attribute is not a valid attribute or already included')
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'
