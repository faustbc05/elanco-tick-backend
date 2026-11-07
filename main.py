from fastapi import FastAPI, Query, HTTPException
from database import get_sightings_page
from datetime import date

app = FastAPI()


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
