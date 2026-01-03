from sqlalchemy import Column, Integer, String, Float, Text, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

# User profile model
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    education = Column(String)
    skills = Column(Text)  # comma-separated string for MVP
    projects = Column(Text)  # JSON or comma-separated
    interests = Column(Text)

    # relationship to career predictions
    # predictions = relationship("CareerPrediction", back_populates="user")


# # Career prediction model
# class CareerPrediction(Base):
#     __tablename__ = "career_predictions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)  # link to UserProfile
#     career_name = Column(String)
#     probability = Column(Float)
#     reasoning = Column(Text)

#     # relationship back to user
#     user = relationship("UserProfile", back_populates="predictions")


# # Market data model
# class MarketData(Base):
#     __tablename__ = "market_data"

#     id = Column(Integer, primary_key=True, index=True)
#     career_name = Column(String, unique=True)
#     average_salary = Column(Float)
#     growth_score = Column(Float)
#     stability_score = Column(Float)
#     job_trends = Column(Text)  # JSON string or CSV for MVP
