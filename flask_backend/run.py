# native imports

from os import getenv

# local imports

from backend import create_app

# generate the flask application for deployment
flask_app = create_app()

# run the application
if __name__ == "__main__":
    flask_app.run(debug=getenv("FLASK_DEBUG", True))
