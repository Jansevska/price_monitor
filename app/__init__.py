from flask import Flask



# Create an instance of Flask class
app = Flask(__name__)
# Configuring our app with Attributes and Values from the Config class --> CREATED AFTER CREATION OF FORMS!!!! <-- app.config['SECRET_KEY'] = 'you-will-never-guess > moved to config.py folder!
# app.config.from_object(Config)


# import routes
from . import routes