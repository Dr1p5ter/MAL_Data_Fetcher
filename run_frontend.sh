#!/bin/bash

# go into the frontend directory
cd react_frontend

# check to see if the packages need installed
if [ ! -d "node_modules" ]; then
    npm install
fi

# run the frontend
npm run dev