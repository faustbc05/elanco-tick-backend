from fastapi import FastAPI, Query, HTTPException
from database import (
    get_sightings_page,
    get_location_counts,
    get_region_counts,
    get_weekly_trends,
    get_monthly_trends,
    initialise_database,
)
from insights import detect_monthly_anomalies
from datetime import date
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/sightings")
def sightings(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    location: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=422, detail="Start date cannot be later than end date"
        )
    result = get_sightings_page(limit, offset, location, start_date, end_date)
    return result


@app.get("/analytics/locations")
def analytics_locations():
    result = get_location_counts()
    return result


@app.get("/analytics/regions")
def analytics_regions():
    result = get_region_counts()
    return result


@app.get("/analytics/trends/weekly")
def analytics_trends_weekly():
    result = get_weekly_trends()
    return result


@app.get("/analytics/trends/monthly")
def analytics_trends_monthly():
    result = get_monthly_trends()
    return result


@app.get("/analytics/insights/anomalies")
def analytics_insights_anomalies():
    monthly_data = get_monthly_trends()
    return detect_monthly_anomalies(monthly_data)
