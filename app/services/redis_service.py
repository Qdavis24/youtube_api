import redis
from app.config import config


redis_client = redis.from_url(config.REDIS_URL)