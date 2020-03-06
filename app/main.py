import logging

from fastapi import FastAPI

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
