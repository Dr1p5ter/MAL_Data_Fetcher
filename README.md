# MAL_Data_Fetcher - React/Flask MAL API Interface

This is an open source MAL API interface that allows for easy use and deployment on local machines. There will be changes coming soon where I will build containers for each part of this app. It will allow for a login to be generated, caching queries for faster lookup times, and request queues. My plan for this project is to deploy it using AWS and post a link to my project.

## Future of the project

A big thing I plan on creating is a request queue feature and PostgreSQL connectivity. I additionally want each of my components to be placed in docker containers. More information on that will come in the later future.

## Installation

Cloning the repository will provide a bunch of files for you and most of them are modifyable. Please pay attention to how each end of development has been set up.

### Backend

The backend for this interface uses Flask which is a low level python microframework used for its quick deployment and creative freedom. A few notes before running because the bash script will not work if a few things are not changed. The path to physically get to acces the native python package must be able to be accessed calling 'python3' in the terminal. Simply call the following to check to see if things are working properly:

```bash
# The python version this app is developed for is version 3.12 and up.
python3 --version
```

In order to set the backend up direct yourself to a bash terminal and please run the following commands in the home directory:

```bash
./run_backend.sh
```

This will automatically check for the dependencies for python and install them. It will continue to run the flask container. The port the backend is hosted on should remain on port 10001 for development purposes. Build ports will not be included within this documentation.

#### Database Implementation
```py
# TODO: This will come at a later date :D
```

### Frontend

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