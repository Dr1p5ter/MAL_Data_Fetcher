# native imports

from json import dump, load
from os import makedirs
from requests import post, Response, get, HTTPError
from secrets import token_urlsafe
from termcolor import colored

# local imports

from fetcher_api.constants import *

class TokenFileNotFoundError(Exception) :
    """
    TokenFileNotFoundError : Token file was not found
    """
    def __init__(self, message : str) :
        self.message = colored(message, WARNING)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class TokenValidationError(Exception) :
    """
    TokenValidationError : Token validation flagged for mismatched API id/secret combo
    """
    def __init__(self, message : str) :
        self.message = colored(message, DANGER)
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

def getCodeVerifier() -> str :
    """
    getCodeVerifier : generates a code verifier/challenge

    Info:
        https://datatracker.ietf.org/doc/html/rfc7636#section-4.1
        https://datatracker.ietf.org/doc/html/rfc7636#section-4.2

    Returns:
        the string for the code verifier/challenge
    """
    return token_urlsafe(100)[:128]

def getAuthorizationCode(client_id : str, code_challenge : str) -> str :
    """
    getAuthorizationCode : initializes a new authorization code for the API to
    use upon runtime.

    Arguments:
        client_id -- API client id
        code_challenge -- the code generated for our token

    Returns:
        The authorization code for the API
    """
    # handmake the url
    url : str = f'{MAL_OAUTH2_ENDPOINT}/authorize?response_type=code&client_id={client_id}&code_challenge={code_challenge}'
    
    # print information to terminal for authorization
    print("To authorise this application please click the following link: ")
    print(url)
    print("(Please check the code generated in the localhost url)\n")

    # gather input from the terminal for the code
    return input('Enter code here: ').strip()

def loadTokenData() -> dict :
    """
    loadTokenData : Grab the token data from token.json

    Raises:
        TokenFileNotFoundError: When the original token file is missing or
        needs generated.
        UnhandledException: An exception occured that was not forseen.

    Returns:
        The token stored in the file.
    """
    try :
        makedirs(METADATA_PATH, exist_ok=True)
        with open(TOKEN_PATH, 'r') as file :
            token : dict = load(file)
        return token
    except FileNotFoundError :
        raise TokenFileNotFoundError("Token file was not found")
    except Exception as UnhandledException :
        raise UnhandledException

def getAPIToken(client_id : str, client_secret : str) -> dict :
    """
    getAPIToken : Generate a token used by the API service

    Arguments:
        client_id -- API client id
        client_secret -- API client secret

    Raises:
        UnhandledException: An exception occured that was not forseen.

    Returns:
        Dictionary object containing token data
    """
    # establish data and the url to grab the token
    url : str = str(f'{MAL_OAUTH2_ENDPOINT}/token')
    verifier : str = getCodeVerifier()
    data : dict = {
        'client_id' : client_id,
        'client_secret' : client_secret,
        'code' : getAuthorizationCode(client_id, verifier),
        'code_verifier' : verifier,
        'grant_type' : 'authorization_code'
    }

    # send a post request to MAL using the data we aquired
    response : Response = post(url, data)
    response.raise_for_status()

    # grab the token and close the response
    token : dict = response.json()
    response.close()
    print("Token has been generated successfully")

    # write the token to the directory
    print("Writing the token to disk...")
    try :
        makedirs(METADATA_PATH, exist_ok=True)
        with open(TOKEN_PATH, 'w') as file :
            dump(token, file, indent = 4)
    except Exception as UnhandledException :
        raise UnhandledException
    print(f"Token successfully wrote to disk! Token stored in {TOKEN_PATH}")

    # return the token contents
    return token

def refreshAPIToken(client_id : str, client_secret : str) -> dict :
    """
    refreshAPIToken : refresh API token upon a 401 error code

    Arguments:
        client_id -- API client id
        client_secret -- API client secret

    Raises:
        UnhandledException: An exception occured that was not forseen.

    Returns:
        current new token that was wrote to disk
    """
    # try to get the old token
    try :
        old_token = loadTokenData()
    except TokenFileNotFoundError :
        # token just needs to be generated
        try :
            token = getAPIToken(client_id, client_secret)
            return token
        except Exception as UnhandledException :
            # underlying issue needs raised up the stack
            raise UnhandledException
    except Exception as UnhandledException :
        # underlying issue needs raised up the stack
        raise UnhandledException
    
    # establish data and the url to grab the token
    url : str = str(f'{MAL_OAUTH2_ENDPOINT}/token')
    data : dict = {
        'client_id' : client_id,
        'client_secret' : client_secret,
        'grant_type' : 'refresh_token',
        'refresh_token' : old_token['refresh_token'],
    }

    # send a post request to MAL using the data we aquired
    response : Response = post(url, data)
    response.raise_for_status()

    # grab the token and close the response
    token : dict = response.json()
    response.close()
    print("Token has been generated successfully")

    # update the token to the directory
    print("Updating the token to disk...")
    try :
        makedirs(METADATA_PATH, exist_ok=True)
        with open(TOKEN_PATH, 'w') as file :
            dump(token, file, indent = 4)
    except Exception as UnhandledException :
        raise UnhandledException
    print(f"Token successfully updated to disk! New token stored in {TOKEN_PATH}")

    # return the token contents
    return token

def validateToken(access_token : str) -> None :
    """
    validateToken : Verifies the usability of the current token stored

    Arguments:
        access_token -- access token present in the current token.json file

    Raises:
        TokenValidationError: Unauthorized use of current token or other 400
        code was thrown upon response call.
        UnhandledException: An exception occured that was not forseen.
    """
    # attempt to perform a simple GET response using the current token and API credentials
    try :
        url : str = 'https://api.myanimelist.net/v2/users/@me'
        response : Response = get(url, 
                    headers = {'Authorization': f'Bearer {access_token}'})
        response.raise_for_status()
        response.close()
    except HTTPError :
        if response.status_code == 401 :
            raise TokenValidationError("Unauthorized use of current stored token")
        else :
            raise TokenValidationError("Other 400 code was raised upon validation")
    except Exception as UnhandledException :
        raise UnhandledException
