from sklearn.ensemble import IsolationForest


def detect_monthly_anomalies(monthly_data):
    if len(monthly_data) < 12:
        return []

    features = [[item["count"]] for item in monthly_data]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )

    predictions = model.fit_predict(features)

    anomalies = []
    for item, prediction in zip(monthly_data, predictions):
        if prediction == -1:
            anomalies.append(
                {
                    "month": item["month"],
                    "count": item["count"],
                }
            )

    return anomalies
