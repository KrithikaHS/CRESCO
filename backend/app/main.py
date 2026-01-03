from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.models import UserProfile #,CareerPrediction, MarketData
from app.routes import profile

app = FastAPI(title="CRESCO Backend")

# Create all tables
Base.metadata.create_all(bind=engine)
app.include_router(profile.router)
@app.get("/")
def root():
    return {"message": "CRESCO backend running"}
