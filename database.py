import sqlite3
from pathlib import Path
from validation import is_valid_sighting
from fetch_data import fetch_sightings

DB_PATH = Path(__file__).parent / "data" / "sightings.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    return connection


def sync_sightings():
    connection = get_connection()

    connection.execute("""
    CREATE TABLE IF NOT EXISTS sightings (
        id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        species TEXT NOT NULL,
        latinName TEXT NOT NULL
    );
    """)

    sightings = fetch_sightings()
    if not isinstance(sightings, list):
        print("Failed to fetch sightings from API")
        connection.close()
        raise SystemExit(1)

    skipped = 0
    for sighting in sightings:
        if not is_valid_sighting(sighting):
            skipped += 1
            continue

        connection.execute(
            """
        INSERT INTO sightings (id, date, location, species, latinName)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (id) DO UPDATE SET
            date = excluded.date,
            location = excluded.location,
            species = excluded.species,
            latinName = excluded.latinName
        """,
            (
                sighting["id"],
                sighting["date"],
                sighting["location"],
                sighting["species"],
                sighting["latinName"],
            ),
        )

    connection.commit()

    cursor = connection.execute("SELECT COUNT(*) FROM sightings")
    row = cursor.fetchone()
    print(f"{row[0]} stored, {skipped} skipped")

    connection.close()


def get_sightings_page(limit, offset, location=None, start_date=None, end_date=None):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    query = """
    SELECT id, date, location, species, latinName
    FROM sightings
    WHERE 1=1
    """

    params = []

    if location is not None:
        query += " AND location = ?"
        params.append(location)

    if start_date is not None:
        query += " AND substr(date, 1, 10) >= ?"
        params.append(start_date.isoformat())

    if end_date is not None:
        query += " AND substr(date, 1, 10) <= ?"
        params.append(end_date.isoformat())

    query += """
    ORDER BY date DESC, id ASC
    LIMIT ? OFFSET ?
    """

    params.extend([limit, offset])

    cursor = connection.execute(query, params)

    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(dict(row))

    connection.close()
    return result


if __name__ == "__main__":
    sync_sightings()
