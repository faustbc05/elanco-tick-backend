from insights import detect_monthly_anomalies


def test_monthly_anomaly_detection():
    monthly_data = [
        {"month": f"2023-{month:02d}", "count": 5} for month in range(1, 13)
    ]

    monthly_data[6]["count"] = 100

    result = detect_monthly_anomalies(monthly_data)

    assert result == [{"month": "2023-07", "count": 100}]


def test_insufficient_monthly_data():
    monthly_data = [
        {"month": "2024-01", "count": 10},
        {"month": "2024-02", "count": 20},
    ]

    result = detect_monthly_anomalies(monthly_data)

    assert result == []
