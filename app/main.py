from fastapi import FastAPI
from app.api.endpoints import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ParkPredict API")

app.include_router(predict.router, prefix="/api")

origins = [
    "http://localhost:5173",  
    "https://sjsuparkpredict.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],  # Only allows GET requests
    allow_headers=["application/json"],  # Only allows 'application/json' header
)