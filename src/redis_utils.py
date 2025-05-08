import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

tokenBlackList = redis.Redis (
    host = Config.REDIS_HOST,
    port = Config.REDIS_PORT,
    db = 0
)

async def addToBlackList(jti: str)->None:
    await tokenBlackList.set(name=jti, value="", ex=JTI_EXPIRY)

async def TokenInBlackList(jti: str) -> bool:
    Isjti = await tokenBlackList.get(jti)

    return Isjti is not None