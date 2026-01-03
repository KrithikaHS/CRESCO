from fastapi import APIRouter, HTTPException
from app.schemas.schemas import MarketDataResponse, MarketDataCreate
from functools import lru_cache
import csv
import os

router = APIRouter(
    prefix="/market",
    tags=["Market Intelligence"]
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/market_data.csv")

# ---- Load CSV data into memory ----
def load_market_data():
    market_data = []
    if not os.path.exists(DATA_FILE):
        print(f"CSV file not found: {DATA_FILE}")
        return market_data

    with open(DATA_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_data = {
                "career_name": row["career_name"],
                "average_salary": float(row["average_salary"]),
                "growth_score": float(row["growth_score"]),
                "stability_score": float(row["stability_score"]),
                "job_trends": [trend.strip() for trend in row["job_trends"].split(";") if trend.strip()]
            }
            # Normalize 0-100
            row_data["growth_score"] = min(max(row_data["growth_score"], 0), 100)
            row_data["stability_score"] = min(max(row_data["stability_score"], 0), 100)
            # Compute simple market-fit score (average of normalized metrics)
            row_data["market_fit"] = round(
                (row_data["average_salary"]/1e5*50 + row_data["growth_score"]*0.25 + row_data["stability_score"]*0.25),
                2
            )
            market_data.append(row_data)
    return market_data

# ---- Cached loader ----
@lru_cache(maxsize=1)
def get_market_data():
    return load_market_data()

# ---- GET all careers ----
@router.get("/", response_model=list[MarketDataResponse])
def list_all_careers():
    return get_market_data()

# ---- GET /market/{career_name} ----
@router.get("/{career_name}", response_model=MarketDataResponse)
def read_market_data(career_name: str):
    data = get_market_data()
    career_name_lower = career_name.strip().lower()
    for row in data:
        if row["career_name"].lower() == career_name_lower:
            return row
    raise HTTPException(status_code=404, detail=f"No market data found for '{career_name}'")

# ---- POST /market ----
@router.post("/", response_model=MarketDataResponse)
def create_market_data(payload: MarketDataCreate):
    data = get_market_data()

    # Check if career exists
    for row in data:
        if row["career_name"].lower() == payload.career_name.lower():
            raise HTTPException(status_code=400, detail="Career already exists")

    # Build new entry
    new_row = {
        "career_name": payload.career_name,
        "average_salary": payload.average_salary,
        "growth_score": min(max(payload.growth_score, 0), 100),
        "stability_score": min(max(payload.stability_score, 0), 100),
        "job_trends": payload.job_trends or [],
    }
    new_row["market_fit"] = round(
        (new_row["average_salary"]/1e5*50 + new_row["growth_score"]*0.25 + new_row["stability_score"]*0.25),
        2
    )
    data.append(new_row)

    # Optional: persist to CSV
    fieldnames = ["career_name", "average_salary", "growth_score", "stability_score", "job_trends"]
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            row_copy = row.copy()
            row_copy["job_trends"] = ";".join(row_copy["job_trends"])
            writer.writerow(row_copy)

    # Clear cache so next GET uses updated data
    get_market_data.cache_clear()

    return new_row
