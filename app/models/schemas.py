from pydantic import BaseModel
from datetime import datetime

class QuickPredictions(BaseModel):
    next_30_mins: dict  # predictions from all garages for next 30 mins
    next_60_mins: dict 
    next_120_mins: dict  

class QuickPredictionResponse(BaseModel):
    timestamp: datetime  # same timestamp as in request
    predictions: QuickPredictions  # predictions for next 30 mins, 1 hour, and 2 hours
    prediction_time: float  # time in secs taken to make prediction

class PredictionResponse(BaseModel):
    timestamp: datetime  
    predictions: dict  
    prediction_time: float  

class AllModelsPredictionResponse(BaseModel):
    timestamp: datetime
    predictions: dict  # every garage prediction for all models
    prediction_time: float
