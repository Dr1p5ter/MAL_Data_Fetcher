# native imports

from dataclasses import dataclass
from json import dump, load
from os import makedirs
from requests import post, Response, get, HTTPError
from secrets import token_urlsafe
from termcolor import colored

# local imports

from fetcher_api.constants import *

class TokenFileNotFoundError(Exception) :
    """
    TokenFileNotFoundError (exception)
    
    Token file was not found.
    """
    def __init__(self, message : str) :
        self.message = colored(message, WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class TokenValidationError(Exception) :
    """
    TokenValidationError (exception)
    
    Token validation flagged for mismatched API id/secret combo.
    """
    def __init__(self, message : str, code : int) :
        self.message = colored(message, DANGER)
        self.code = code
        super().__init__(f'{self.message} - {self.code}')
    
    def __str__(self) :
        return f'{self.message} - {self.code}'

@dataclass(init=False)
class APIToken :
    """
    (class object)

    A container for the API token information and should be called to make API
    communication easier to initialize. It is required to pass in the API key
    to begin.
    
    Raises
    ------
    HTTPError
        Bad http response occured when sending a post request to the MAL API
        gateway.
    TokenValidationError
        400-404 error code was raised.
    """

    _token : dict[str, str]

    def __init__(self, key : tuple[str, str]):
        # attempt to get the token if it is stored on disc
        try :
            token = self._loadTokenData()
        except TokenFileNotFoundError :
            # attemp to grab the token through manually submitting a request
            try :
                token = self._getAPIToken(key[0], key[1])
            except HTTPError as error :
                raise HTTPError
        
        # validate the token before proceeding with initialization
        object.__setattr__(self, '_token', token)
        try :
            self._validateToken(self._token['access_token'])
        except TokenValidationError as error :
            # check if the token needs to be refreshed
            if error.code == 401 :
                try :
                    new_token = self._refreshAPIToken(key[0], key[1], self._token['refresh_token'])
                except HTTPError :
                    raise error
                object.__setattr__(self, '_token', new_token)
        
    def getToken(self) -> dict :
        """
        getToken (public method)

        Helper for returning the token.

        Returns
        -------
        dict
            A dictionary containing token data.

        Attributes
        ----------
        token_type
            Type of token as a string.
        expires_in
            Amount of time till the token expires from creation as an int.
        access_token
            Access token as a string.
        refresh_token
            Refresh token as a string.        
        """
        return self._token

    def _loadTokenData(self) -> dict :
        """
        _loadTokenData (private method)

        Grab the token data from token.json file.

        Returns
        -------
        dict
            The token stored in the file.

        Attributes
        ----------
        token_type
            Type of token as a string.
        expires_in
            Amount of time till the token expires from creation as an int.
        access_token
            Access token as a string.
        refresh_token
            Refresh token as a string.        

        Raises
        ------
        TokenFileNotFoundError
            When the original token file is missing or needs generated.
        """
        try :
            makedirs(METADATA_PATH, exist_ok=True)
            with open(TOKEN_PATH, 'r') as file :
                token : dict = load(file)
            return token
        except FileNotFoundError :
            raise TokenFileNotFoundError("Token file was not found")

    def _getAPIToken(self, client_id : str, client_secret : str) -> dict :
        """
        _getAPIToken (private method)

        Generate a token used by the API service.

        Parameters
        ----------
        client_id : str
            API client id.
        client_secret : str
            API client secret.

        Returns
        -------
        dict
            Dictionary object containing token data.
        
        Attributes
        ----------
        token_type
            Type of token as a string.
        expires_in
            Amount of time till the token expires from creation as an int.
        access_token
            Access token as a string.
        refresh_token
            Refresh token as a string.

        Raises
        ------
        HTTPError
            Bad http response occured when sending a post request to the MAL
            API gateway.
        """
        # get verifier code
        verifier : str = token_urlsafe(100)[:128]

        # get auhorization code
        url : str = f'{MAL_OAUTH2_ENDPOINT}/authorize?response_type=code&client_id={client_id}&code_challenge={verifier}'
        
        # print information to terminal for authorization
        print("To authorise this application please click the following link: ")
        print(url)
        print("(Please check the code generated in the localhost url)\n")

        # gather input from the terminal for the code
        auth_code = input('Enter code here: ').strip()

        # establish data and the url to grab the token
        url : str = str(f'{MAL_OAUTH2_ENDPOINT}/token')
        data : dict = {
            'client_id' : client_id,
            'client_secret' : client_secret,
            'code' : auth_code,
            'code_verifier' : verifier,
            'grant_type' : 'authorization_code'
        }

        # send a post request to MAL using the data we aquired
        try :
            response : Response = post(url, data)
            response.raise_for_status()
        except HTTPError :
            raise HTTPError

        # grab the token and close the response
        token : dict = response.json()
        response.close()
        print("Token has been generated successfully")

        # write the token to the directory
        print("Writing the token to disk...")
        makedirs(METADATA_PATH, exist_ok=True)
        with open(TOKEN_PATH, 'w') as file :
            dump(token, file, indent = 4)
        print(f"Token successfully wrote to disk! Token stored in {TOKEN_PATH}")

        # return the token contents
        return token

    def _refreshAPIToken(self, client_id : str, client_secret : str, refresh_token : str) -> dict :
        """
        _refreshAPIToken (private method)

        Refresh API token upon a 401 error code.

        Parameters
        ----------
        client_id : str
            API client id.
        client_secret : str
            API client secret.
        refresh_token : str
            API refresh token.

        Returns
        -------
        dict
            Current new token that was wrote to disk.

        Attributes
        ----------
        token_type
            Type of token as a string.
        expires_in
            Amount of time till the token expires from creation as an int.
        access_token
            Access token as a string.
        refresh_token
            Refresh token as a string.

        Raises
        ------
        HTTPError
            Bad http response occured when sending a post request to the MAL
            API gateway.
        """
        # establish data and the url to grab the token
        url : str = str(f'{MAL_OAUTH2_ENDPOINT}/token')
        data : dict = {
            'client_id' : client_id,
            'client_secret' : client_secret,
            'grant_type' : 'refresh_token',
            'refresh_token' : refresh_token,
        }

        # send a post request to MAL using the data we aquired
        try :
            response : Response = post(url, data)
            response.raise_for_status()
        except HTTPError :
            raise HTTPError

        # grab the token and close the response
        new_token : dict = response.json()
        response.close()
        print("Token has been generated successfully")

        # update the token to the directory
        print("Updating the token to disk...")
        makedirs(METADATA_PATH, exist_ok=True)
        with open(TOKEN_PATH, 'w') as file :
            dump(new_token, file, indent = 4)
        print(f"Token successfully updated to disk! New token stored in {TOKEN_PATH}")

        # return the token contents
        return new_token

    def _validateToken(self, access_token : str) -> None :
        """
        _validateToken (private method)

        Verifies the usability of the current token stored.

        Parameters
        ----------
        access_token : str
            API access token.

        Raises
        ------
        TokenValidationError
            400-404 error code was raised.
        """
        # attempt to perform a simple GET response using the current token and API credentials
        try :
            url : str = 'https://api.myanimelist.net/v2/users/@me'
            response : Response = get(url, 
                        headers = {'Authorization': f'Bearer {access_token}'})
            response.raise_for_status()
            response.close()
        except HTTPError :
            match (response.status_code) :
                case 400 :
                    raise TokenValidationError("Invalid parameters detected", response.status_code)
                case 401 :
                    # attempt to refresh to try and fix it
                    return TokenValidationError("Invalid/Expired token", response.status_code)
                case 403 :
                    raise TokenValidationError("DoD detected", response.status_code)
                case 404 :
                    raise TokenValidationError("Invalid Path/File Not Found", response.status_code)