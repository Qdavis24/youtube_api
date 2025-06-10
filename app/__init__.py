from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from flask import Blueprint
import dotenv

dotenv.load_dotenv()



api_bp = Blueprint("api", __name__)

from . import routes



def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(api_bp)

    return app