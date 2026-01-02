from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.models import UserProfile, CareerPrediction, MarketData


app = FastAPI(title="CRESCO Backend")

# Create all tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "CRESCO backend running"}
