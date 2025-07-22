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

ml_model = {
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
        global ml_model
        self.available_models = ml_model.keys()

    def load_ml_model(self, model_name, probabilistic=False):
        global ml_model
        if model_name not in ml_model.keys():
            raise ValueError("model not found")
        if ml_model[model_name] is None:
            logger.info(f"loading {model_name} model from pickles/")
            # load model from pickle file
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "pickles", model_name)
            if probabilistic:
                file_path = os.path.join(file_path, f"{model_name}_p.pkl")
            else:
                file_path += os.path.join(file_path, f"{model_name}.pkl")
            with model_lock:
                if ml_model[model_name] is None:
                    ml_model[model_name] = joblib.load(file_path)

        return ml_model[model_name]
    
    def clean_prediction(self, prediction):
        if prediction < 0:
            return 0.0
        elif prediction > 100:
            return 100.0
        else:
            return round(prediction, 1)
    
    def ml_model(self, model_name, minutes, garage, prob=True):
        minutes = np.array(minutes).reshape(1, -1)
        model = self.load_ml_model(model_name, probabilistic=prob)
        prediction = round(model[garage].predict(minutes).flatten()[0], 1)
        return self.clean_prediction(prediction)
    
    def production_model(self, timestamp, garage):
        return self.ml_model("random_forest", timestamp, garage)
    
model_helper = ModelHelper()

def get_model_helper():
    return model_helper