import logging

from typing import List, Optional
from fastapi import FastAPI
from starlette import status as sc
from fastapi import HTTPException
from app import __version__
from app.config import KidsApiConfig
from app.models import KidsPredictionRequest, KidsPredictionResponse

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
    response = requests.get(url=ml_ping_url)
    if response.status_code == sc.HTTP_200_OK:
        return 'pong'
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )


@app.post(path='/ml/predictions', description='ML based predictions for Kickstarter campaign success',
          response_model=List[KidsPredictionResponse])
def ml_predict(requests: List[KidsPredictionRequest]) -> Optional[List[KidsPredictionResponse]]:
    import requests as req
    import pandas as pd
    from fastapi.encoders import jsonable_encoder

    ml_predictions_url = f'{config.model_url}/invocations'
    ml_requests = [r.to_ml_request() for r in requests]
    formatted_requests = pd.DataFrame.from_records(ml_requests).to_json(orient='split')
    logger.info(formatted_requests)
    payload = jsonable_encoder(formatted_requests)
    ml_response = req.post(url=ml_predictions_url, data=payload,
                        headers={'Content-type': 'application/json; format=pandas-split'})
    if ml_response.status_code == sc.HTTP_200_OK:
        ml_predictions = ml_response.json()
        response_data = zip(requests, ml_predictions)
        return [KidsPredictionResponse(prediction=prediction, **request.dict()) for request, prediction in
                response_data]
    else:
        raise HTTPException(
            status_code=ml_response.status_code,
            detail=f'Non valid response from ml predictions endpoint. ml response: {ml_response.text}'
        )

