from flask import Blueprint, jsonify, request
from datetime import datetime

from models.sinusoidal import predict_sinusoidal
from utils.time_utils import get_minutes_from_week_start

predictions_bp = Blueprint('predictions', __name__)

# In-memory storage for predictions history
prediction_history = []

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
        prediction = predict_sinusoidal(minutes, data['garage'])
        
        # Store prediction in history
        prediction_record = {
            "timestamp": data['timestamp'],
            "garage": data['garage'],
            "predicted_fullness": prediction,
            "prediction_time": datetime.now().isoformat()
        }
        prediction_history.append(prediction_record)
        
        return jsonify(prediction_record)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500