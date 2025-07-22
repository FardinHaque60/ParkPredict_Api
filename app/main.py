from fastapi import FastAPI
from app.api.endpoints import predict

app = FastAPI(title="ParkPredict API")

app.include_router(predict.router, prefix="/api")