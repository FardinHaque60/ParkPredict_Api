from flask import Flask
import os
import sys

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    from routes.main import main_bp
    from routes.predictions import predictions_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(predictions_bp)
    
    return app

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)