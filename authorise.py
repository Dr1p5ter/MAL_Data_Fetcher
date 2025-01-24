from json import dump, load
from requests import post, Response
from secrets import token_urlsafe

MAL_oauth2_link = 'https://myanimelist.net/v1/oauth2'
token_filepath = 'token.json'

class TokenFileNotFoundError(Exception) :
    """
    TokenFileNotFoundError : Token file was not found
    """
    def __init__(self, message : str) :
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.message}'

class StaleTokenError(Exception) :
    """
    StaleTokenError : Token has expired and needs refreshed
    """
    def __init__(self, message : str) :
        self.message = message
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
    url : str = f'{MAL_oauth2_link}/authorize?response_type=code&client_id={client_id}&code_challenge={code_challenge}'
    
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
        with open(token_filepath, 'r') as file :
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
    url : str = str(f'{MAL_oauth2_link}/token')
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
        with open(token_filepath, 'w') as file :
            dump(token, file, indent = 4)
    except Exception as UnhandledException :
        raise UnhandledException
    print(f"Token successfully wrote to disk! Token stored in {token_filepath}")

    # return the token contents
    return token

def refreshAPIToken(client_id : str, client_secret : str) -> dict :
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
    url : str = str(f'{MAL_oauth2_link}/token')
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
        with open(token_filepath, 'w') as file :
            dump(token, file, indent = 4)
    except Exception as UnhandledException :
        raise UnhandledException
    print(f"Token successfully updated to disk! New token stored in {token_filepath}")

    # return the token contents
    return token
