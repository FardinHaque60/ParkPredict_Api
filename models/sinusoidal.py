import numpy as np

from utils.time_utils import get_minutes_from_week_start
from utils.state import sinusoidal_params

def sinusoidal_model(x, A, B, C, D):
    """Sinusoidal function for curve fitting."""
    return A * np.sin(B * x + C) + D

def predict_sinusoidal(minutes: float, garage: str) -> float:
    """
    Make prediction using sinusoidal model for specified garage
    """
    try:
        if garage not in sinusoidal_params:
            raise ValueError(f"Predictions not available for {garage}. Currently only supporting: {', '.join(sinusoidal_params.keys())}")
        
        params = sinusoidal_params[garage]
        prediction = sinusoidal_model(minutes, *params)
        return float(prediction)
    except Exception as e:
        print(f"Error in predict_sinusoidal: {str(e)}")
        raise 