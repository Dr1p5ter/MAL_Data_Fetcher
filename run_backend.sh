#!/bin/bash

# exit on error
set -e

# go into the backend subdirectory
cd flask_backend

# Activate virtual environment (if applicable)
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
else 
    echo "Continuing without virtual enviornment"
fi

# Running a check for requirements.txt
python3 -m pip install -v -r requirements.txt --no-cache-dir

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file was not found in flask_backend, exiting now"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -q -h $PG_HOST -p $PG_PORT; then
    echo "PostgreSQL is NOT running on $PG_HOST:$PG_PORT! Please start it first."
    exit 1
else
    echo "PostgreSQL is running on $PG_HOST:$PG_PORT!"
fi

# Run database migrations
echo "Checking for database migrations..."
if [ ! -d "migrations" ]; then
    echo "No migration history found, initializing migrations..."
    flask db init
fi

echo "Generating new migrations"
python3 -Bm flask db migrate -m "Auto-migration" || echo "No new migrations detected."

echo "Applying database migrations..."
python3 -Bm flask db upgrade

# Start Flask app
echo "Starting Flask backend..."
python3 -Bm flask run --host=$FLASK_HOST --port=$FLASK_PORT
