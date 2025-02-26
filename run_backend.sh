#!/bin/bash

# download required modules
python3 -m pip install -r requirements.txt

# run app
python3 -m flask_backend.app
