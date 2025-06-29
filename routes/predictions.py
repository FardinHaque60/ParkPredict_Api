from flask import Blueprint, jsonify, request
from datetime import datetime

from models.model_helper import ModelHelper
from utils.time_utils import get_minutes_from_week_start
import traceback

predictions_bp = Blueprint('predictions', __name__)

MODELS = ["decision_tree", "gam", "guassian", "knn", "random_forest"]
model_helper = ModelHelper()

@predictions_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if 'timestamp' not in data:
            return jsonify({
                "error": "Missing required field: timestamp"
            }), 400
            
        if 'garage' not in data:
            return jsonify({
                "error": "Missing required field: garage"
            }), 400
        
        # Parse timestamp
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return jsonify({
                "error": "Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            }), 400
        
        # Get minutes from week start
        minutes = get_minutes_from_week_start(timestamp)
        
        # Make prediction
        predictions = []
        for model in MODELS:
            pred = -1
            if model == "sine":
                pred = model_helper.sine_model(minutes, data['garage']) 
            else:
                pred = model_helper.ml_model(model, minutes, data['garage'])
            predictions.append(pred)
        print(f"LOG: prediction: {predictions}")
        
        # Store prediction in history
        # TODO: stream this data so the client receives each prediction without waiting on everything
        prediction_record = {
            "timestamp": data['timestamp'],
            "garage": data['garage'],
            "predicted_fullness_list": predictions,
            "prediction_time": datetime.now().isoformat()
        }
        
        return jsonify(prediction_record)
        
    except Exception:
        print("ERROR: \n\n")
        traceback.print_exc()
        return jsonify({"error": "error occurred"}), 500