import os
from fastapi import FastAPI
import logging
from pydantic import BaseModel

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger('uvicorn.error')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

LIGHT_ON = False

@app.get("/")
def home():
    return {"messenger": "By HoangTrung"}

@app.get("/light")
def get_light():
    return LIGHT_ON

class LightOn(BaseModel):
    on: bool

@app.post("/light")
def post_light(light_on: LightOn):
    global LIGHT_ON
    logger.info(f"Setting light to {bool(light_on.on)}")
    LIGHT_ON = bool(light_on.on)
    return LIGHT_ON
