import json
from pathlib import Path
from datetime import datetime, timedelta
import logging
import tempfile

logger = logging.getLogger(__name__)

CACHE_DIR = Path("data")
CACHE_DIR.mkdir(exist_ok=True)

CACHE_FILE = CACHE_DIR / "weather_cache.json"
TTL_MINUTES = 30


# ---------------------- INTERNAL HELPERS ----------------------

def _load_all():
    """
    Load the entire cache file safely.
    Handles corruption, missing file, and unexpected errors.
    """
    if not CACHE_FILE.exists():
        return {}

    try:
        with CACHE_FILE.open("r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        logger.error("⚠ Cache file corrupted — resetting weather_cache.json")
        try:
            CACHE_FILE.unlink()
        except Exception:
            pass
        return {}

    except Exception as e:
        logger.error(f"Unexpected error loading cache: {e}")
        return {}


def _save_all(cache_dict: dict):
    """
    Atomically save the full JSON dictionary.
    Prevents partial writes from corrupting the file.
    """
    try:
        with tempfile.NamedTemporaryFile(
            "w", delete=False, dir=CACHE_DIR, suffix=".tmp"
        ) as tmp:
            json.dump(cache_dict, tmp, indent=2)
            temp_name = tmp.name

        Path(temp_name).replace(CACHE_FILE)
        logger.info("Cache file updated safely.")

    except Exception as e:
        logger.error(f"⚠ Failed to write cache file: {e}")


# ---------------------- PUBLIC FUNCTIONS ----------------------

def load_cache(city: str):
    """
    Load cached data for one city.
    Returns:
        payload, previous_temp
    TTL expiration returns:
        (None, stale_payload)
    """
    cache = _load_all()

    if city not in cache:
        logger.info(f"No cache entry for: {city}")
        return None, None

    entry = cache[city]

    # Parse timestamp
    try:
        ts = datetime.fromisoformat(entry.get("timestamp", ""))
    except Exception:
        logger.error(f"Invalid timestamp for '{city}' — ignoring cache entry.")
        return None, entry.get("payload")

    # TTL expiration
    if datetime.now() - ts > timedelta(minutes=TTL_MINUTES):
        logger.warning(f"Cache expired for '{city}' — returning stale data only.")
        return None, entry.get("payload")

    return entry.get("payload"), entry.get("previous")


def save_cache(city: str, payload: dict):
    """
    Save cached payload for one city inside shared JSON cache.
    Stores:
        - timestamp
        - payload
        - previous temperature (for trend detection)
    """
    cache = _load_all()

    previous_temp = (
        cache.get(city, {})
        .get("payload", {})
        .get("temperature")
    )

    cache[city] = {
        "timestamp": datetime.now().isoformat(),
        "payload": payload,
        "previous": previous_temp,
    }

    _save_all(cache)
