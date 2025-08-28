from fastapi import APIRouter
from app.utils.supabase_client import read_data_from_supabase
from datetime import datetime

router = APIRouter()

@router.get("/data")
def data(garage: str, day: str):
    real_data = read_data_from_supabase("real_data", garage=garage, day=day)
    prediction_data = read_data_from_supabase("random_forest_predictions", garage=garage, day=day)

    # Assuming each entry in real_data has a 'timestamp' field as a string
    for entry in real_data:
        if 'timestamp' in entry:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], "%Y-%m-%d %I:%M:%S %p").isoformat()

    for entry in prediction_data:
        if 'timestamp' in entry:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], "%Y-%m-%d %I:%M:%S %p").isoformat()

    real_data.sort(key=lambda x: x['timestamp'])
    prediction_data.sort(key=lambda x: x['timestamp'])

    return {
        "actual_data": real_data,
        "prediction_data": prediction_data
    }