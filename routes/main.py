from flask import Blueprint, render_template, jsonify

from utils.state import sinusoidal_params

main_bp = Blueprint('main', __name__)

# List of all available garages
ALL_GARAGES = ["North Garage", "South Garage", "West Garage"]

# endpoint to render home page
@main_bp.route('/')
def home():
    return render_template('index.html', 
                         all_garages=ALL_GARAGES,
                         available_garages=list(sinusoidal_params.keys()))