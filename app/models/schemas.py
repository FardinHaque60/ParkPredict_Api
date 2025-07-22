from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    timestamp: datetime  # same timestamp as in request
    garage: str   # same garage as in request
    prediction: float  # predicted fullness percentage
    prediction_time: float  # time in secs taken to make prediction

class AllPredictionsResponse(BaseModel):
    timestamp: datetime
    garage: str   
    predictions_list: dict  # list of predictions from all models
    prediction_time: float 
