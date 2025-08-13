# ParkPredict API

A FastAPI for predicting parking lot fullness with endpoints using various models.

## Running the API

### Pre-check
1. Activate venv via `source venv/bin/activate`
2. install dependencies `pip install -r requirements.txt`
Note: app can also be built with `docker build`

### Running
1. Run FastAPI app by running `uvicorn app.main:app --reload`
3. The API will be available at `http://localhost:8000/docs` to test endpoints

## Project Structure

```
ParkPredict/app/
├── api/                 
│   └── endpoints/       # api endpoints
├── ml_models/           # model binary files + loading logic
├── models/              # schemas for endpoint requests and responses
├── utils/               # helper methods
├── main.py              # app entry point
```

## API Endpoints

### GET /predict
- expects: `?timestamp={datetime in iso format}`
- response: 
```
{
  timestamp: datetime     # same timestamp as in request
  predictions: float       # predicted fullness percentage
  prediction_time: float  # time in secs taken to make prediction
}
```

### GET /predict_all
- expects: same format as above
- response: same as above, expect there is a dictionary for every model

## ML Model Handling
models are saved in binaries called pickles which are decoded using a library called joblib. The model helper class is a singleton that lazily loads models as requests come and saves them in memory to use for later requests.
- `ml_models/load_models.py`: contains singleton class definition and getter method
- `ml_models/pickles.py`: contains binaries that models are loaded from