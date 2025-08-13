from fastapi import FastAPI
from app.api.endpoints import predict, sms_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ParkPredict API")

app.include_router(predict.router, prefix="/api")
app.include_router(sms_routes.router, prefix="/sms")

origins = [
    "http://localhost:5173",  
    "https://sjsuparkpredict.vercel.app",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"], 
    allow_headers=["application/json"],  
)