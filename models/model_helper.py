'''
singleton class for loading model. 

TODO look into adding singleton tag from render
'''
import pickle
import os
import numpy as np

class ModelHelper:
    AVAILABLE_MODELS = {"decision_tree", "gam", "guassian", "knn", "random_forest"}
    models = {}

    # TODO: make singleton so model is loaded once per thread, etc.
    def use_model(self, model_name, probabilistic=False):
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError("model not found")
        if model_name not in self.models:
            print("LOG: loading model from pickles/")
            # load model from pickle file
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "pickles", model_name)
            if probabilistic:
                file_path = os.path.join(file_path, f"{model_name}_p.pkl")
            else:
                file_path += os.path.join(file_path, f"{model_name}.pkl")
            with open(file_path, "rb") as f:
                self.models[model_name] = pickle.load(f)

        return self.models[model_name]
    
    def ml_model(self, model_name, timestamp, garage, prob=True):
        timestamp = np.array(timestamp).reshape(1, -1)
        model = self.use_model(model_name, probabilistic=prob)
        return round(model[garage].predict(timestamp).flatten()[0], 1)
    
    def production_model(self, timestamp, garage):
        return self.ml_model("random_forest", timestamp, garage)