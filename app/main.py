import logging

from fastapi import FastAPI
from starlette import status as sc
from fastapi import HTTPException
from app import __version__
from app.config import KidsApiConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kids.api')
config: KidsApiConfig = KidsApiConfig.load()

app = FastAPI(
    title=config.name,
    description=config.description,
    version=__version__,
    debug=False
)


@app.get(path='/ping', description='Healthcheck endpoint')
def ping():
    return 'pong'


@app.get(path='/ml/ping', description='Machine learning endpoint healthcheck')
def ml_ping():
    import requests
    ml_ping_url = f'{config.model_url}/ping'
    logger.info(ml_ping_url)
    response = requests.get(url=ml_ping_url)
    if response.status_code == sc.HTTP_200_OK:
        return 'pong'
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )