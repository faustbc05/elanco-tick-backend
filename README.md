# Elanco Tick Sightings Backend

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
- **scikit-learn:** Provides Isolation Forest for detecting unusual historical monthly sighting counts.

## Architecture

The backend separates data ingestion from API request handling.

During synchronisation, `fetch_data.py` retrieves sightings from the external Elanco API and handles retrieval errors. The records are processed by `database.py`, which uses `validation.py` to reject invalid data before inserting or updating records in local SQLite storage.

Separately, `main.py` defines the FastAPI endpoints. These endpoints call database functions to retrieve, filter and aggregate previously stored sightings, returning the results as JSON.

For anomaly detection, `insights.py` analyses the monthly counts returned by `database.py` using Isolation Forest.

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

`.\.venv
