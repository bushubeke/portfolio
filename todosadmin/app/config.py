import os
#from dotenv import load_dotenv 
# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv('.env')

class Config(object):
    
    
    SECRET_KEY='96bc95204c20d462b014a064d5595d368c51601f0b1addd603c00cb4ad2d3be9353506a8c37608f5106bcbd85e42f1bd26665a7cef2605a93297c82b321fcdab'
    DEBUG = False


class ProductionConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'todos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
      
  

   
config_by_name = dict(
   
    prod=ProductionConfig
)

key = Config.SECRET_KEY