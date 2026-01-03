from pydantic import BaseModel
from typing import List, Optional

# User profile input
class UserProfileBase(BaseModel):
    name: str
    email: str
    education: str
    skills: List[str]
    projects: List[str]
    interests: List[str]

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRes(UserProfileBase):
    id: int
    class Config:
        orm_mode = True


# Career prediction output
class CareerPredictionBase(BaseModel):
    career_name: str
    probability: float
    reasoning: str

class CareerPrediction(CareerPredictionBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True


# Market data schema
class MarketDataBase(BaseModel):
    career_name: str
    average_salary: float
    growth_score: float
    stability_score: float
    job_trends: Optional[List[str]] = None

class MarketData(MarketDataBase):
    id: int
    class Config:
        orm_mode = True

class MarketDataResponse(BaseModel):
    career_name: str
    average_salary: float
    growth_score: float
    stability_score: float
    job_trends: List[str]

    class Config:
        from_attributes = True  # Pydantic v2

class MarketDataCreate(BaseModel):
    career_name: str
    average_salary: float
    growth_score: float
    stability_score: float
    job_trends: Optional[List[str]] = []
