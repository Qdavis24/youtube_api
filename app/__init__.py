import dotenv
dotenv.load_dotenv()

from flask import Flask
from app.config import config
from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS





api_bp = Blueprint("api", __name__)

from . import routes


limiter = Limiter(key_func=get_remote_address, default_limits=["120 per minute"], storage_uri=config.REDIS_URL)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    limiter.init_app(app)
    app.register_blueprint(api_bp)

    return app