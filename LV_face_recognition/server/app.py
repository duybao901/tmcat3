from flask import Flask
import os
import configparser
from App.factory import create_app
import cherrypy

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))

# app = Flask(__name__)

# @app.route('/')
# def index():
#   return "Hello world"

if __name__ == "__main__":
  app = create_app()
  
  app.config['MONGO_URI'] = "mongodb+srv://baoduy123:baoduy123@cluster0.ubjer5c.mongodb.net/face-data?retryWrites=true&w=majority"
  cherrypy.tree.graft(app.wsgi_app, '/')
  cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 5000,
                        'engine.autoreload.on': False,
                        })
  cherrypy.engine.start()

  
  