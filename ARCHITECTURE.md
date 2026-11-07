# Architecture and Design Decisions

## System Overview

The Elanco Tick Sightings Backend is a Python application that retrieves historical sighting data from an external API, validates and persists the records in SQLite, and exposes search and analytics functionality through FastAPI.

The system separates data ingestion from API request handling so that stored sightings remain accessible even if the external data source becomes unavailable.

## Application Components

| Component | Responsibility |
|---|---|
| `fetch_data.py` | Retrieves data from Elanco's API, using an HTTP timeout and handling common network and response errors |
| `validation.py` | Validates required sighting fields and timestamp formats |
| `database.py` | Initialises SQLite, synchronises sightings, performs parameterised queries and calculates analytics |
| `regions.py` | Maps known UK locations to regions |
| `main.py` | Exposes FastAPI endpoints and validates incoming request parameters |
| `tests/test_api.py` | Tests API behaviour, startup, analytics, invalid requests and data preservation during outages |

## Data Ingestion

Synchronisation requests the latest available dataset from the external API. Invalid records are skipped, while valid records are inserted or updated using their unique sighting IDs.

SQLite UPSERT operations prevent duplicate IDs from creating duplicate database records. Database transactions allow pending changes to be rolled back if an unexpected error occurs.

## API Request Flow

When a client requests sighting data, FastAPI validates the query parameters and calls the corresponding database function.

Sighting searches use parameterised SQL queries to apply location, date and pagination filters. Aggregated reports group sightings by location, mapped region, week or month.

Results are returned as JSON. The application does not need to contact Elanco's external API for each read request.

## Reliability

The backend includes HTTP timeout handling, data validation, transaction rollback and database connection cleanup.

If synchronisation fails before records are imported, previously committed sightings remain available. Automated tests use temporary databases and mocked external API responses to verify key reliability behaviour.

## Technology Decisions

FastAPI was chosen for its straightforward endpoint definitions, automatic input validation and generated API documentation.

SQLite was chosen to keep the assessment self-contained and easy to install without a dedicated database server.

Python provides a common language across ingestion, validation, persistence, analytics and automated testing.

## Trade-offs and Future Improvements

The current design prioritises simplicity, reproducibility and reliable data processing.

Potential improvements include scheduled synchronisation, database indexes, more flexible geographical mapping, improved operational monitoring, and migration to a server-based database for greater concurrency.

Historical sighting counts should not be interpreted as verified current disease-risk predictions.