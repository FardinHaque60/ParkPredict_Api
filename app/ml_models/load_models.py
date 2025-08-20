'''
singleton class for loading model. 
'''
import os
import numpy as np
import logging
import joblib
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PRODUCTION_MODEL = "random_forest"  # change name of model to use a different model in production endpoints
GARAGES = ["North Garage", "South Garage", "West Garage"]
ML_MODELS = {
    "decision_tree": None, 
    "gam": None, 
    "guassian": None, 
    "knn": None, 
    "random_forest": None
}
model_lock = threading.Lock()

class ModelHelper:
    available_models = []

    def __init__(self):
        global ML_MODELS
        self.available_models = ML_MODELS.keys()

    def load_ml_model(self, model_name, probabilistic=False):
        global ML_MODELS
        if model_name not in ML_MODELS.keys():
            raise ValueError("model not found")
        if ML_MODELS[model_name] is None:
            logger.info(f"loading {model_name} model from pickles/")
            # load model from pickle file
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "pickles", model_name)
            if probabilistic:
                file_path = os.path.join(file_path, f"{model_name}_p.pkl")
            else:
                file_path += os.path.join(file_path, f"{model_name}.pkl")
            with model_lock:
                if ML_MODELS[model_name] is None:
                    ML_MODELS[model_name] = joblib.load(file_path)

        return ML_MODELS[model_name]
    
    def clean_prediction(self, prediction) -> float:
        if prediction < 0:
            return 0.0
        elif prediction > 100:
            return 100.0
        else:
            return round(prediction)
    
    def ml_model(self, model_name, minutes, prob=True) -> dict:
        minutes = np.array(minutes).reshape(1, -1)
        model = self.load_ml_model(model_name, probabilistic=prob)
        predictions = {}
        for garage in GARAGES:
            predictions[garage] = self.clean_prediction(round(model[garage].predict(minutes).flatten()[0], 1))
        return predictions
    
    def production_model(self, timestamp) -> dict:
        return self.ml_model(PRODUCTION_MODEL, timestamp)
    
model_helper = ModelHelper()

def get_model_helper():
    return model_helper