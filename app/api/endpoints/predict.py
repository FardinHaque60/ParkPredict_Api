# TODO update endpoints to stream responses
from fastapi import APIRouter
from app.models.schemas import PredictionResponse, AllPredictionsResponse
from app.utils.lib import get_minutes_from_week_start
from app.ml_models.load_models import get_model_helper
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

model_helper = get_model_helper()
MODELS = model_helper.available_models

@router.get("/predict", response_model=PredictionResponse)
def predict(timestamp: datetime, garage: str):
    logger.info(f"params for predict request: timestamp={timestamp}, garage={garage}")

    # Get minutes from week start
    minutes = get_minutes_from_week_start(timestamp)
    
    # Make prediction
    start_time = datetime.now()
    prediction = model_helper.production_model(minutes, garage)
    end_time = datetime.now()
    logger.info(f"prediction: {prediction}")
    
    # return prediction object
    prediction_time = int((end_time - start_time).total_seconds() * 1000)
    prediction_record = {
        "timestamp": timestamp,
        "garage": garage,
        "prediction": prediction,
        "prediction_time": prediction_time
    }
    
    return prediction_record

# returns predictions for all models
@router.get("/predict_all", response_model=AllPredictionsResponse)
def predict_all(timestamp: datetime, garage: str):
    logger.info(f"params for predict request: timestamp={timestamp}, garage={garage}")

    # Get minutes from week start
    minutes = get_minutes_from_week_start(timestamp)
    
    # Make predictions
    predictions = {}
    start_time = datetime.now()
    for model in MODELS:
        predictions[model] = model_helper.ml_model(model, minutes, garage)
    end_time = datetime.now()
    logger.info(f"predictions: {predictions}")
    
    # return prediction object
    prediction_time = int((end_time - start_time).total_seconds() * 1000)
    prediction_record = {
        "timestamp": timestamp,
        "garage": garage,
        "predictions_list": predictions,
        "prediction_time": prediction_time
    }
    
    return prediction_record