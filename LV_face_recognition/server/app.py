
import os
import configparser
from App.factory import create_app
from sklearn.neighbors import KNeighborsClassifier

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))

if __name__ == "__main__":
  app = create_app()
  app.config['MONGO_URI'] = config['PROD']['DB_URI']  
 
  app.run(debug=True)      

  
  