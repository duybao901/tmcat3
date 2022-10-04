
import os
import configparser
from flask_pymongo import PyMongo
from App.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))

if __name__ == "__main__":
  app = create_app()
  app.config['MONGO_URI'] = config['PROD']['DB_URI']  
  app.run(debug=True)      

  
  