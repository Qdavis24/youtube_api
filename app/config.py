import os



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REDIS_URL = os.environ.get("REDIS_URL")

class DevelopmentConfig(Config):
    DEBUG = True
    PROXY = None

class ProductionConfig(Config):
    DEBUG = False
    PROXY = f"http://{os.environ.get('PROXY_USERNAME')}:{os.environ.get('PROXY_PASSWORD')}@p.webshare.io:{os.environ.get('PROXY_PORT')}"

# CHANGE FOR DEPLOYMENT TO PRODUCTION SERVER
config = DevelopmentConfig