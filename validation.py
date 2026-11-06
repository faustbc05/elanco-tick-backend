from datetime import datetime


def is_valid_sighting(sighting):
    if isinstance(sighting, dict) == False:
        return False

    if (
        sighting.get("id") is None
        or not isinstance(sighting.get("id"), str)
        or sighting.get("id").strip() == ""
    ):
        return False

    required_fields = (
        "date",
        "location",
        "species",
        "latinName",
    )

    for field in required_fields:
        value = sighting.get(field)

        if not isinstance(value, str) or value.strip() == "":
            return False

    try:
        datetime.strptime(sighting["date"], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False

    return True
