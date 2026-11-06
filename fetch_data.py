import requests

API_URL = "https://dev-task.elancoapps.com/data/tick-sightings"


def fetch_sightings():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        sightings = response.json()

        return sightings
    except requests.exceptions.Timeout as error:
        print(f"API request timed out: {error}")
    except requests.exceptions.HTTPError as error:
        print(f"HTTP returned an error: {error}")
    except requests.exceptions.JSONDecodeError as error:
        print(f"JSON failed to decode: {error}")
    except requests.exceptions.ConnectionError as error:
        print(f"Connection to Server Failed: {error}")

    return None
