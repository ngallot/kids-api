from pydantic import BaseModel
from typing import Optional


class KidsPredictionRequest(BaseModel):
    country: str
    currency: str
    days_campaign: int
    hours_prepa: float
    goal: float

    def to_ml_request(self):
        return {
            'country_clean': self.country,
            'currency_clean': self.currency,
            'days_campaign': self.days_campaign,
            'hours_prepa': self.hours_prepa,
            'goal': self.goal
        }


class KidsPredictionResponse(KidsPredictionRequest):
    prediction: bool
