"""
🔴 Redis Client
Manejo de conexión a Redis para caché
"""

import redis.asyncio as redis
from app.core.config import settings
from loguru import logger

# Cliente global
redis_client: redis.Redis = None

async def get_redis_pool() -> redis.Redis:
    """
    Crea y devuelve el pool de conexiones a Redis
    """
    global redis_client
    if redis_client is None:
        logger.info(f"🔌 Conectando a Redis: {settings.REDIS_URL}")
        redis_client = redis.from_url(
            settings.REDIS_URL, 
            encoding="utf-8", 
            decode_responses=True
        )
    return redis_client

async def close_redis_pool():
    """
    Cierra la conexión a Redis
    """
    global redis_client
    if redis_client:
        logger.info("🔌 Cerrando conexión a Redis...")
        await redis_client.close()
        redis_client = None
