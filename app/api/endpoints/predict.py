from fastapi import APIRouter
from app.models.schemas import PredictionResponse, AllModelsPredictionResponse, QuickPredictionResponse
from app.utils.lib import get_minutes_from_week_start
from app.ml_models.load_models import get_model_helper
from app.utils.supabase_client import write_log_to_supabase
import logging
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

model_helper = get_model_helper()
MODELS = model_helper.available_models

# PRODUCTION endpoint to make prediction for all garages
@router.get("/predict", response_model=PredictionResponse)
def predict(timestamp: datetime):
    logger.info(f"params for predict request: timestamp={timestamp}")

    try:
        # log prediction request time
        time = timestamp.strftime("%I:%M %p")
        # log request time
        pacific = timezone(timedelta(hours=-7))
        timestamp = datetime.now(pacific)
        timestamp_str = timestamp.strftime("%Y-%-m-%-d %I:%M:%S %p")
        write_log_to_supabase(timestamp_str, time)
        logger.info(f"logged custom time input to supabase: {time}")
    except IndexError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"failed to log time to supabase: {e}")

    # Get minutes from week start
    minutes = get_minutes_from_week_start(timestamp)
    
    # Make prediction
    start_time = datetime.now()
    predictions = model_helper.production_model(minutes)
    end_time = datetime.now()
    logger.info(f"prediction: {predictions}")
    
    # return prediction object
    prediction_time = round((end_time - start_time).total_seconds(), 4)
    prediction_record = {
        "timestamp": timestamp,
        "predictions": predictions,
        "prediction_time": prediction_time
    }
    
    return prediction_record

# PRODUCTION endpoint to return predictions for the next 30 mins, 1 hour, and 2 hours
@router.get("/quick_predict", response_model=QuickPredictionResponse)
def quick_predict(timestamp: datetime):
    logger.info(f"params for quick_predict request: timestamp={timestamp}")

    # Get minutes from week start
    minutes = get_minutes_from_week_start(timestamp)
    
    # Make predictions
    start_time = datetime.now()
    predictions = {}
    for interval in [30, 60, 120]:  # 30 mins, 1 hour, 2 hours    
        predictions[f"next_{interval}_mins"] = model_helper.production_model(minutes + interval)
    end_time = datetime.now()
    logger.info(f"predictions: {predictions}")
    
    # return prediction object
    prediction_time = round((end_time - start_time).total_seconds(), 4)
    prediction_record = {
        "timestamp": timestamp,
        "predictions": predictions,
        "prediction_time": prediction_time
    }
    
    return prediction_record

# GENERAL endpoint that returns predictions from all models
@router.get("/predict_all", response_model=AllModelsPredictionResponse)
def predict_all(timestamp: datetime):
    logger.info(f"params for predict_all request: timestamp={timestamp}")

    # Get minutes from week start
    minutes = get_minutes_from_week_start(timestamp)
    
    # Make predictions
    predictions = {}
    start_time = datetime.now()
    for model in MODELS:
        predictions[model] = model_helper.ml_model(model, minutes)
    end_time = datetime.now()
    logger.info(f"predictions: {predictions}")
    
    # return prediction object
    prediction_time = round((end_time - start_time).total_seconds(), 4)
    prediction_record = {
        "timestamp": timestamp,
        "predictions": predictions,
        "prediction_time": prediction_time
    }
    
    return prediction_record