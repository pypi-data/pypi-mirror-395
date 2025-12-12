import urllib.request
import urllib.error
import json
import logging

# Simple mapping of city names to coordinates.
# You can add more cities here easily.
CITY_COORDS: dict[str, tuple[float, float]] = {
    "delhi": (28.6, 77.2),
    "pune": (18.52, 73.86),
    "mumbai": (19.07, 72.88),
    "bangalore": (12.97, 77.59),
    "bengaluru": (12.97, 77.59),
    "kolkata": (22.57, 88.36),
    "chennai": (13.08, 80.27),
    "hyderabad": (17.38, 78.49),
}


def get_coords_for_city(city: str, default_lat: float, default_lon: float) -> tuple[float, float]:
    """Return (lat, lon) for a given city name if known,
    otherwise fall back to defaults from config/CLI."""
    coords = CITY_COORDS.get(city.lower())
    if coords:
        return coords
    logging.warning(f"No predefined coordinates for city '{city}', using default lat/lon")
    return default_lat, default_lon


def fetch_weather(lat: float, lon: float) -> dict | None:
    """Fetch current weather for given coordinates using Open-Meteo."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    logging.debug(f"Requesting URL: {url}")

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                logging.error(f"HTTP Error: {resp.status}")
                return None

            raw = resp.read()
            data = json.loads(raw)
            return data.get("current_weather")

    except urllib.error.HTTPError as e:
        logging.error(f"HTTP error: {e}")
    except urllib.error.URLError as e:
        logging.error(f"Network error: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

    return None


if __name__ == "__main__":
    # quick manual test
    print(fetch_weather(28.6, 77.2))
