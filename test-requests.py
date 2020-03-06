import requests
from fastapi.encoders import jsonable_encoder


def test_ml_ping():
    url = 'http://localhost:1234/ping'
    response = requests.get(url=url)
    print(response.status_code)


def test_ml_invocations():
    """
    country: str
    currency_clean: str
    days_campaign: int
    hours_prepa: float
    goal: float
    """

    data = [{
        "country_clean": "US",
        "currency_clean": "USD",
        "days_campaign": 10,
        "hours_prepa": 2.0,
        "goal": 2500.0
    }]

    import pandas as pd

    df = pd.DataFrame.from_records(data)
    payload = jsonable_encoder(df.to_json(orient='split'))
    print(payload)
    response = requests.post(url='http://0.0.0.0:1234/invocations', data=payload,
                             headers={"Content-type": "application/json; format=pandas-split"})
    print(f'Status code: {response.status_code}')
    if response.status_code != 200:
        print(response.text)
    else:
        print(response.json())


def test_ml_endpoint():
    data = [{
        "country": "US",
        "currency": "USD",
        "days_campaign": 10,
        "hours_prepa": 2.0,
        "goal": 2500.0
    }]
    response = requests.post(url='http://localhost:8000/ml/predictions', json=jsonable_encoder(data))
    print(f'Status code: {response.status_code}')
    if response.status_code != 200:
        print(response.text)
    else:
        print(response.json())


if __name__ == '__main__':
    try:
        test_ml_endpoint()
    except Exception as e:
        print(str(e))
