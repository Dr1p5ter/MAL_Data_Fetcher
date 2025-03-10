# MAL_Data_Fetcher - React/Flask MAL API Interface

This is an open source MAL API interface that allows for easy use and deployment on local machines. There will be changes coming soon where I will build containers for each part of this app. It will allow for a login to be generated, caching queries for faster lookup times, and request queues. My plan for this project is to deploy it using AWS and post a link to my project.

## Future of the project

A big thing I plan on creating is a request queue feature. I additionally want each of my components to be placed in docker containers. More information on that will come in the later future.

# Installation

Cloning the repository will provide a bunch of files for you and most of them are modifyable. Please pay attention to how each end of development has been set up.

## Backend

The backend for this interface uses Flask which is a low level python microframework used for its quick deployment and creative freedom. A few notes before running because the bash script will not work if a few things are not changed. The path to physically get to acces the native python package must be able to be accessed calling 'python3' in the terminal. Simply call the following to check to see if things are working properly:

```bash
# The python version this app is developed for is version 3.12 and up.
python3 --version
```

### Configuration for Backend
***This is an extremely important step for beginning the bash script. Flask has a lot of variables it depends on and it is necessary for runtime completion. Please pay attention to the names (order does not matter). This file should be stord within the '/flask_backend' directory as '.env' to ensure the bash script can access it. Additionally, set your virtual enviornment (.venv) in the same directory. This step is optional and not required. *** 

### Flask Configs
```bash
# Python config
PYTHONDONTWRITEBYTECODE=1

# Flask configuration
FLASK_APP="run.py"
FLASK_ENV="development"
FLASK_HOST="localhost"
FLASK_PORT=10001
FLASK_DEBUG=True
FLASK_SKIP_DOTENV=1

# Secret Key for application
SECRET_KEY=...

# Frontend configs
REACT_HOST='localhost'
REACT_PORT=10002
```
For the most part the only variables I would recommend changing is the host and port variables for deployment on other services. The only **required** enviornment variable needed for your own deployment is the *SECRET_KEY* variable. This should be a 64 byte string or hash. Do not share these.

### PostgreSQL Configs
```bash
# Database configuration for postgresql
DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<db_name>"
PG_HOST="localhost"
PG_PORT=10000

# Model configs

USER_USERNAME_MAX_LEN=80
USER_PASSWORD_MAX_LEN=200
USER_EMAIL_MAX_LEN=80
USER_FNAME_MAX_LEN=32
USER_M1NAME_MAX_LEN=32
USER_M2NAME_MAX_LEN=32
USER_LNAME_MAX_LEN=32
USER_NNAME_MAX_LEN=16
USER_BIO_MAX_LEN=200
USER_COUNTRY_MAX_LEN=100
USER_STATE_PROVINCE_MAX_LEN=100
USER_REC_QUESTION_MAX_LEN=100
USER_REC_ANSWER_MAX_LEN=32
```
These variables are configurable to where you are hosting the database. The URL will need to be modified for your convenience before running the bash script. Any Model configs (there will be more in the future), is necessary for SQLAlchemy to set up migrations and the tables. I advise only making the variables themselves bigger and not smaller.

### Running the Backend
In order to set the backend up direct yourself to a bash terminal and please run the following commands in the home directory outside of flask_backend subdirectory:

```bash
./run_backend.sh
```

This will automatically check for the dependencies for python and install them. It will continue to run the flask container. The port the backend is hosted on should remain on port 10001 for development purposes. Build ports will not be included within this documentation.

### Frontend

>#### DISCLAIMER: This is a work in progress and I won't publish functioality until I get a feature working smoothly. The script will still run but nothing will happen. Sorry for the inconvenience. I take security seriously and want to make sure every instance of routing is handled first.

The frontend is hosted using React.js and Vite.js together. It is ran using npm version 11.1.0 and up but for the best results when forking try to only use this version. Vite is ran on version 6.1.0 on this build.

To deploy the frontend simply go into a different bash terminal and type the following commands in the home directory:

```bash
./run_frontend.sh
```

The script will check to make sure packages are installed correctly as well. The port the frontend is hosted on should remain on port 10002 for development purposes. Build ports will not be included within this documentation.

## Contact

Feel free to contact me regarding any questions you might have!

**Name:** *Matthew McLaren*  
**Business Email:** *mmclaren2021@outlook.com*