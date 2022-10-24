import enum
from fastapi import FastAPI
import logging
from pydantic import BaseModel
import aioredis
import config

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger("uvicorn.error")
# logger.addHandler(handler)
logger.setLevel(logging.INFO)

KEY = "light"

app = FastAPI()
redis = aioredis.Redis.from_url(config.REDIS_URI)


@app.get("/")
async def home():
    return {"messenger": "By HoangTrung"}


@app.get("/light")
async def get_light():
    value = await redis.get(KEY)
    if value is None:
        await redis.set(KEY, 0)
        value = 0
    return bool(int(value))


class LightOnState(int, enum.Enum):
    one = 1
    off = 0


class LightOn(BaseModel):
    on: LightOnState


@app.post("/light")
async def post_light(light_on: LightOn):
    value = int(light_on.on)
    logger.info(f"Setting light to {value}")
    await redis.set(KEY, value)
    logger.info(f"Light value set to {value}")
    return value
