import database
from fastapi.testclient import TestClient
from main import app
import pytest


def test_startup_and_health(tmp_path, monkeypatch):
    temporary_db = tmp_path / "sightings.db"

    monkeypatch.setattr(
        database,
        "DB_PATH",
        temporary_db,
    )

    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

        response = client.get("/sightings")

        assert response.status_code == 200
        assert response.json() == []

    assert temporary_db.exists()


def test_invalid_sightings_filters(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DB_PATH",
        tmp_path / "sightings.db",
    )

    invalid_urls = [
        "/sightings?limit=0",
        "/sightings?limit=101",
        "/sightings?offset=-1",
        "/sightings?start_date=2024-12-31&end_date=2024-01-01",
    ]

    with TestClient(app) as client:
        for url in invalid_urls:
            response = client.get(url)

            assert response.status_code == 422
        response = client.get("/sightings?start_date=2024-01-01&end_date=2024-01-01")
        assert response.status_code == 200
        assert response.json() == []


def test_analytics_with_known_data(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DB_PATH",
        tmp_path / "sightings.db",
    )

    with TestClient(app) as client:
        connection = database.get_connection()

        test_sightings = [
            ("T1", "2024-01-01T12:00:00", "Manchester", "Sheep tick", "Ixodes ricinus"),
            ("T2", "2024-01-03T16:00:00", "Manchester", "Sheep tick", "Ixodes ricinus"),
            ("T3", "2024-01-08T08:00:00", "London", "Sheep tick", "Ixodes ricinus"),
            ("T4", "2024-02-01T09:00:00", "Manchester", "Sheep tick", "Ixodes ricinus"),
        ]

        connection.executemany(
            """
            INSERT INTO sightings
                (id, date, location, species, latinName)
            VALUES (?, ?, ?, ?, ?)
            """,
            test_sightings,
        )
        connection.commit()
        connection.close()

        response = client.get("/analytics/locations")
        assert response.status_code == 200
        assert response.json() == [
            {"location": "Manchester", "count": 3},
            {"location": "London", "count": 1},
        ]

        response = client.get("/analytics/regions")
        assert response.status_code == 200
        assert response.json() == [
            {"region": "North West", "count": 3},
            {"region": "London", "count": 1},
        ]

        response = client.get("/analytics/trends/weekly")
        assert response.status_code == 200
        assert response.json() == [
            {"week_start": "2024-01-01", "count": 2},
            {"week_start": "2024-01-08", "count": 1},
            {"week_start": "2024-01-29", "count": 1},
        ]

        response = client.get("/analytics/trends/monthly")
        assert response.status_code == 200
        assert response.json() == [
            {"month": "2024-01", "count": 3},
            {"month": "2024-02", "count": 1},
        ]


def test_sync_failure_preserves_data(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database,
        "DB_PATH",
        tmp_path / "sightings.db",
    )

    database.initialise_database()

    connection = database.get_connection()
    connection.execute(
        """
    INSERT INTO sightings (id, date, location, species, latinName)
    VALUES (?, ?, ?, ?, ?)
    """,
        (
            "TEST001",
            "2024-01-01T12:00:00",
            "Manchester",
            "Sheep tick",
            "Ixodes ricinus",
        ),
    )

    connection.commit()
    connection.close()

    monkeypatch.setattr(
        database,
        "fetch_sightings",
        lambda: None,
    )

    with pytest.raises(SystemExit) as error:
        database.sync_sightings()
    assert error.value.code == 1

    connection = database.get_connection()
    cursor = connection.execute("SELECT COUNT(*) FROM sightings;")
    result = cursor.fetchone()
    assert result[0] == 1
    connection.close()
