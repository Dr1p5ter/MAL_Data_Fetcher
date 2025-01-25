from os.path import exists

API_key_path : str = 'key.env'
API_client_id_len : int = 32
API_client_secret_len : int = 64

class KeyFileNotFoundError(Exception) :
    """
    KeyFileNotFound : Key file was not found in parent directory
    """
    def __init__(self, message : str) :
        self.message = message
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
        return f'{self.invalid_id} -> {self.message}'
    
class InvalidClientSecretError(Exception) :
    """
    InvalidClientSecretError : Length of client secret was not valid
    """
    def __init__(self, invalid_secret : str, message : str) :
        self.invalid_secret = invalid_secret
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) :
        return f'{self.invalid_secret} -> {self.message}'

def grabAPIInfo() -> tuple[str,str] :
    """
    grabAPIInfo : This function will read the API information that was stored
    in the key.env file in the parent directory. This function will always
    return a tuple unless otherwise an exception occurs within the read
    operation.

    Warning: DO NOT SHARE API KEYS!

    Raises:
        InvalidClientIdError: The client id was of an invalid length.
        InvalidClientSecretError: The client secret was of an invalid length.
        KeyFileNotFoundError: The key.env file was not found in the parent
        directory.
        UnhandledException: An exception occured that was not forseen.

    Returns:
        A tuple object containing the client id followed by the client secret.
        The return type of each will be of class string.
    """
    # try to read the key file
    try :
        # open the file
        with open(API_key_path, 'r') as file :
            # grab the client id from the first line
            API_client_id : str = str(file.readline()).strip()
            if len(API_client_id) != API_client_id_len :
                raise InvalidClientIdError("Client Id was not a valid length")

            # grab the client secret from the second line
            API_client_secret : str = str(file.readline()).strip()
            if len(API_client_secret) != API_client_secret_len :
                raise InvalidClientSecretError("Client Secret was not a valid length")

            # return a tuple containing the (id, secret) pairing
            return (API_client_id, API_client_secret)
    except FileNotFoundError :
        raise KeyFileNotFoundError("Key file was not found in parent directory")
    except Exception as UnhandledException:
        raise UnhandledException

def makeKeyFile() -> None :
    """
    makeKeyFile : verifies that the key file is made and prompts the user to
    input data before any other functionality that requires such information
    begins.

    Raises:
        UnhandledException: An exception occured that was not forseen.
    """
    # check if key file not present in parent directory
    if not exists(API_key_path) :
        # grab the API information to continue
        print("It appears that the key.env file was not present.\n")
        client_id : str = str(input("Please enter the MAL API client Id : ")).strip()
        client_secret : str = str(input("Please enter the MAL API client secret : ")).strip()

        # generate the file so it is present in the directory
        print("Writing the key file into the parent directory...")
        try :
            with open(API_key_path, 'w') as file :
                file.write(f'{client_id}\n{client_secret}')
        except Exception as UnhandledException :
            raise UnhandledException
        print("key.env was successfully written to the parent directory!\n")
