from flask import Blueprint, render_template, jsonify
import sys
import os
import numpy as np

from utils.state import sinusoidal_params

main_bp = Blueprint('main', __name__)

# List of all available garages
ALL_GARAGES = ["North Garage", "South Garage", "West Garage", "South Campus Garage"]

def load_sinusoidal_params():
    """
    Load sinusoidal parameters for all garages
    """
    SIN_COEFFICIENTS = np.array([5.38809038e+01, 4.36672403e-03, 5.00665498e+02, 4.19897973e+01])
    GARAGE_MODELS = {
        "North Garage": SIN_COEFFICIENTS,
        "South Garage": SIN_COEFFICIENTS,
        "West Garage": SIN_COEFFICIENTS,
        "South Campus Garage": SIN_COEFFICIENTS
    }
    try:
        params = GARAGE_MODELS
        # Update the global parameters with all available garages
        sinusoidal_params.clear()
        sinusoidal_params.update(params)
        print(f"Successfully loaded sinusoidal parameters for garages: {', '.join(params.keys())}")
        return True
    except Exception as e:
        print(f"Error loading sinusoidal parameters: {str(e)}")
        return False

@main_bp.route('/')
def home():
    # Load models if not already loaded
    if not sinusoidal_params:
        load_success = load_sinusoidal_params()
        if not load_success:
            return render_template('error.html', 
                                message="Failed to load prediction models. Please try again later.")
    
    return render_template('index.html', 
                         all_garages=ALL_GARAGES,
                         available_garages=list(sinusoidal_params.keys()))

@main_bp.route('/load_models', methods=['POST'])
def load_models_endpoint():
    try:
        success = load_sinusoidal_params()
        if not success:
            return jsonify({
                "error": "Failed to load models. Please check the server logs for details."
            }), 500
            
        return jsonify({
            "status": "success",
            "message": "Sinusoidal parameters loaded successfully",
            "available_garages": list(sinusoidal_params.keys())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/weights', methods=['GET'])
def weights_endpoint():
    """
    Get the sinusoidal regression weights for all garages
    """
    try:
        return jsonify({
            "sinusoidal_regression_weights": {
                garage: params.tolist() 
                for garage, params in sinusoidal_params.items()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500 