## Project Overview

This backend retrieves and processes historical tick-sighting data from the live Elanco Tick Sightings API. It enables users to search and filter sightings by location and date range, with pagination to support efficient data retrieval.

The application also provides aggregated reporting, including sighting counts by city and region, as well as weekly and monthly trends. To improve reliability, it validates incoming records, prevents duplicate sightings through database UPSERT operations, and preserves previously stored data when the external API is unavailable.

The backend exposes these features through a REST API built using FastAPI.

## Technical Stack

The project uses the following technologies:

- **Python:** Provides a consistent language for data fetching, validation, database operations and API functionality, supported by libraries such as Requests and pytest.
- **FastAPI:** Provides HTTP endpoints, automatic request validation, JSON responses and interactive OpenAPI documentation through `/docs`.
- **SQLite:** Provides persistent relational storage without requiring a separate database server. It is suitable for a self-contained technical-assessment MVP and supports efficient SQL filtering and aggregation.
- **pytest:** Provides automated tests for API endpoints, input validation, analytics and database reliability.

## Architecture

The backend separates data ingestion from API request handling.

During synchronisation, `fetch_data.py` retrieves sightings from the external Elanco API and handles retrieval errors. The records are processed by `database.py`, which uses `validation.py` to reject invalid data before inserting or updating records in local SQLite storage.

Separately, `main.py` defines the FastAPI endpoints. These endpoints call database functions to retrieve, filter and aggregate previously stored sightings, returning the results as JSON.

This separation allows the API to continue serving existing records when the external Elanco API is temporarily unavailable. Database tables are initialised when FastAPI starts, while data synchronisation is performed separately.

## Installation and Setup

The following instructions are intended for **Windows PowerShell**. Python 3.10 or later and Git should be installed before proceeding.

### 1. Clone the Repository

Clone the public GitHub repository:

`git clone https://github.com/faustbc05/elanco-tick-backend.git`

Navigate into the project directory:

`cd elanco-tick-backend`

### 2. Create a Python Virtual Environment

Create a virtual environment to isolate the project's dependencies:

`py -m venv .venv`

### 3. Install Dependencies

Install the required Python packages from `requirements.txt`:

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

### 4. Populate the Local Database

Run the synchronisation script to retrieve tick sightings from Elanco's external API, validate the records and store them in SQLite:

`.\.venv\Scripts\python.exe database.py`

The database is created automatically if it does not already exist. Repeated synchronisation updates existing records using their unique IDs without creating duplicates.

**Note:** Synchronisation requires access to the external Elanco API. If retrieval fails, the script reports an error and preserves existing stored records. On a fresh installation, sightings will remain unavailable until synchronisation succeeds.

### 5. Start the FastAPI Server

Launch the development server using Uvicorn:

`.\.venv\Scripts\python.exe -m uvicorn main:app --reload`

The API will be available at `http://127.0.0.1:8000`.

To view and interact with the automatically generated API documentation, open:

[FastAPI Interactive Documentation](http://127.0.0.1:8000/docs)

The server runs continuously until stopped with `Ctrl + C`.

### 6. Run Automated Tests

Open a separate terminal, or stop Uvicorn, and execute:

`.\.venv\Scripts\python.exe -m pytest -v`

The tests cover application initialisation, request validation, analytics calculations and database reliability. Temporary databases and mocked API responses are used to avoid modifying the application's stored sightings.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns the application health status |
| GET | `/sightings` | Retrieves sightings with pagination and optional filters |
| GET | `/analytics/locations` | Returns sighting counts grouped by location |
| GET | `/analytics/regions` | Returns counts grouped by mapped UK region |
| GET | `/analytics/trends/weekly` | Returns sightings grouped by Monday-starting week |
| GET | `/analytics/trends/monthly` | Returns sightings grouped by calendar month |

### Sighting Filters

The `/sightings` endpoint accepts the following optional query parameters:

| Parameter | Default | Description |
|---|---|---|
| `limit` | 50 | Number of sightings returned, between 1 and 100 |
| `offset` | 0 | Number of matching records skipped |
| `location` | None | Exact location name |
| `start_date` | None | Inclusive date filter in YYYY-MM-DD format |
| `end_date` | None | Inclusive date filter in YYYY-MM-DD format |

Example requests:

`GET /sightings?location=London&limit=10&offset=10`

Returns up to ten London sightings after skipping the first ten matching results.

`GET /sightings?start_date=2024-01-01&end_date=2024-02-10`

Returns up to 50 sightings recorded within the specified date range, inclusive.

`GET /sightings?location=London&start_date=2024-01-01&end_date=2024-02-10&limit=10&offset=10`

Combines location filtering, date filtering and pagination.

Invalid limits, negative offsets and reversed date ranges return HTTP 422.

Interactive API documentation is available at `/docs` when the server is running.

## Limitations and Future Improvements

**Geographic coverage:** Region reporting currently relies on a predefined mapping of location names to UK regions. Locations not included in the mapping are classified as `Unknown`. A future implementation could use more comprehensive geographic reference data.

**Scalability:** SQLite is appropriate for this self-contained MVP, but increased data volumes or concurrent usage may benefit from additional database indexes, query optimisation and migration to a server-based database such as PostgreSQL.

**Data availability:** Sightings are synchronised from an external API rather than continuously streamed. New sightings are only available locally following a successful synchronisation.

**Interpretation:** Historical sighting counts indicate records present in the dataset, not verified current tick prevalence or an individual's risk of tick exposure.

**Future development:** Potential improvements include scheduled synchronisation, more comprehensive observability and geographic visualisation.