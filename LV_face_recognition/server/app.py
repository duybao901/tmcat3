from flask import Flask
import os
import configparser
from App.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))
from waitress import serve

# app = Flask(__name__)

# @app.route('/')
# def index():
#   return "Hello world"

if __name__ == "__main__":
  app = create_app()
  app.config['MONGO_URI'] = "mongodb+srv://baoduy123:baoduy123@cluster0.ubjer5c.mongodb.net/face-data?retryWrites=true&w=majority"
  serve(app, host="0.0.0.0", port=5000, url_scheme='http')

  
  