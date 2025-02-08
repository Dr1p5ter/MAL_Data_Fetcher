# native imports

from dataclasses import dataclass
from json import dump, load
from os import makedirs
from os.path import exists
from termcolor import colored

# local imports

from fetcher_api.constants import *

class APIKeyInvalidArgumentError(Exception) :
    """
    APIKeyInvalidArgumentError : Arguments used to initialize APIKey object are invalid or empty
    """
    def __init__(self, message : str, child_error : Exception) :
        self.message = colored(message, DANGER)
        self.child_error = child_error
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}\n{self.child_error}'
    
class KeyFileNotFoundError(Exception) :
    """
    KeyFileNotFound : Key file was not found in parent directory
    """
    def __init__(self, message : str) :
        self.message = colored(message, DANGER)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class InvalidClientIdError(Exception) :
    """
    InvalidClientIdError : Length of client id was not valid
    """
    def __init__(self, invalid_id : str, message : str) :
        self.invalid_id = invalid_id
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) :
        return colored(f'{self.invalid_id} -> {self.message}', DANGER)
    
class InvalidClientSecretError(Exception) :
    """
    InvalidClientSecretError : Length of client secret was not valid
    """
    def __init__(self, invalid_secret : str, message : str) :
        self.invalid_secret = invalid_secret
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) :
        return colored(f'{self.invalid_secret} -> {self.message}', DANGER)

@dataclass(init=False)
class APIKey :
    """
     A container for API key information and should be called to make API
     communication easier to initialize. There is no need to pass any arguments
     into the class. Each value will be initialized through helper methods.

    Raises :
        InvalidClientIdError : Client id was not valid
        InvalidClientSecretError : Client secret was not valid

    Methods :
        getKey() : Returns a tuple containing the stored values
    """
    
    _id : str
    _secret : str

    def __init__(self) :
        # probe the user for API credentials if there have been none provided before runtime
        self._makeKeyFile()

        # grab API information
        
        try :
            data_pair : dict = self._grabAPIInfo()
        except (InvalidClientIdError, InvalidClientSecretError) :
            raise APIKeyInvalidArgumentError
        except KeyFileNotFoundError :
            self._makeKeyFile()
            data_pair : dict = self._grabAPIInfo()
        
        object.__setattr__(self, '_id', data_pair['_id'])
        object.__setattr__(self, '_secret', data_pair['_secret'])
    
    def getKey(self) -> tuple[str, str] :
        """
        getKey : Helper method for returning class data for the key

        Returns:
            A tuple containing strings for the id and secret respectfully
        """
        return (self._id, self._secret)
    
    def _grabAPIInfo(self) -> dict :
        """
        _grabAPIInfo : This function will read the API information that was stored
        in the key file in the parent directory. This function will always
        return a tuple unless otherwise an exception occurs within the read
        operation.

        Warning : DO NOT SHARE API KEYS!

        Raises :
            InvalidClientIdError : The client id was of an invalid length.
            InvalidClientSecretError : The client secret was of an invalid length.
            KeyFileNotFoundError : The key file was not found in the parent
            directory.

        Returns :
            A dictionary object containing the id and secret for the API.
            dict fields :
                _id : The API id
                _secret : The API secret
        """
        # try to read the key file
        try :
            # open the file
            makedirs(METADATA_PATH, exist_ok=True)
            with open(KEY_PATH, 'r') as file :
                key_dict : dict = load(file)

                # grab the client id from the first line
                API_client_id : str = key_dict['_id']
                if len(API_client_id) != API_CLIENT_ID_LEN :
                    raise InvalidClientIdError("Client Id was not a valid length")

                # grab the client secret from the second line
                API_client_secret : str = key_dict['_secret']
                if len(API_client_secret) != API_CLIENT_SECRET_LEN :
                    raise InvalidClientSecretError("Client Secret was not a valid length")

                # return a tuple containing the (id, secret) pairing
                return key_dict
        except FileNotFoundError :
            raise KeyFileNotFoundError("Key file was not found in parent directory")

    def _makeKeyFile(self) -> None :
        """
        _makeKeyFile : verifies that the key file is made and prompts the user to
        input data before any other functionality that requires such information
        begins.
        """
        # check if key file not present in parent directory
        if not exists(KEY_PATH) :
            # grab the API information to continue
            print("It appears that the key file was not present.\n")
            client_id : str = str(input("Please enter the MAL API client Id : ")).strip()
            client_secret : str = str(input("Please enter the MAL API client secret : ")).strip()
            key_data : dict = {
                '_id' : client_id,
                '_secret' : client_secret
            }

            # generate the file so it is present in the directory
            print("Writing the key file into the parent directory...")
            makedirs(METADATA_PATH, exist_ok=True)
            with open(KEY_PATH, 'w') as file :
                dump(key_data, file, indent=4)
            print("key was successfully written to the parent directory!\n")
