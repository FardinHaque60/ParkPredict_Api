from fastapi import APIRouter
from app.utils.supabase_client import read_data_from_supabase, read_south_campus_data_from_supabase
from datetime import datetime

router = APIRouter()

@router.get("/south-campus-data")
def south_campus_data(day: str):
    real_data = read_south_campus_data_from_supabase("actual_south_campus", day=day)

    # Assuming each entry in real_data has a 'timestamp' field as a string
    for entry in real_data:
        if 'timestamp' in entry:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], "%Y-%m-%d %I:%M:%S %p").isoformat()

    real_data.sort(key=lambda x: x['timestamp'])

    return {
        "south_campus_data": real_data,
    }

@router.get("/south-campus-predictions")
def south_campus_predictions(day: str):
    prediction_data = read_south_campus_data_from_supabase("people_prediction_south_campus", day=day)

    # Assuming each entry in prediction_data has a 'timestamp' field as a string
    for entry in prediction_data:
        if 'timestamp' in entry:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], "%Y-%m-%d %I:%M:%S %p").isoformat()
            entry["fullness"] = entry["people"]

    prediction_data.sort(key=lambda x: x['timestamp'])

    return {
        "south_campus_data": prediction_data
    }

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