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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)), log_level="info")
