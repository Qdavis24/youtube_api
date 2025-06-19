import redis
from app.config import config


redis_client = redis.from_url(config.REDIS_URL, max_connections=5, socket_keepalive=True)