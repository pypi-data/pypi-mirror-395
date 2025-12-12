# main.py

from cli import get_args
from config import load_config
from fetcher import fetch_weather, get_coords_for_city
from cache import load_cache, save_cache
from logging_system import setup_logging
from alerts import check_alert
from exporter import export_cache_to_csv, print_cache_as_table

from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import logging
import webbrowser
import re


# --------------------------- MAP UTILITY ---------------------------

def open_map(lat, lon):
    url = f"https://www.google.com/maps?q={lat},{lon}"
    print(f"🗺 Opening map: {url}")
    webbrowser.open(url)


# --------------------------- CITY VALIDATION ---------------------------

def validate_city_name(city: str) -> bool:
    """
    Valid city names contain only letters, spaces, and hyphens.
    Prevents numeric and special-character entries.
    """
    pattern = r"^[A-Za-z\s\-]+$"
    return bool(re.match(pattern, city))


# --------------------------- CITY LIST BUILDER ---------------------------

# def build_city_list(args, cfg) -> list[str]:
#     cities: list[str] = []

#     # -c flag or --city
#     if args.cities:
#         cities.extend(args.cities)

#     # --cities "Delhi,Mumbai"
#     if args.cities_comma:
#         cities.extend([c.strip() for c in args.cities_comma.split(",") if c.strip()])

#     # positional arguments
#     if args.positional_city:
#         cities.extend(args.positional_city)

#     # CSV export before processing
#     if args.export_csv:
#         export_cache_to_csv()

#     # If no input, use config default
#     if not cities:
#         cities = [cfg["city"]]

#     # Validate names
#     valid = []
#     for c in cities:
#         if validate_city_name(c):
#             valid.append(c)
#         else:
#             print(f"\n❌ Invalid city name: {c}")
#             print("Allowed: letters, spaces, hyphens.")
#             print("Example: Delhi, New York, Pune-East")
#             exit(1)

#     return valid
def build_city_list(args, cfg) -> list[str]:
    cities: list[str] = []

    # -c Delhi -c Pune  → args.cities (list)
    if args.cities:
        if isinstance(args.cities, list):
            cities.extend(args.cities)
        else:
            # --cities "Delhi,Mumbai"
            cities.extend([c.strip() for c in args.cities.split(",") if c.strip()])

    # Add positional cities
    if args.positional_city:
        cities.extend(args.positional_city)

    # Export CSV immediately if requested
    if getattr(args, "export_csv", False):
        export_cache_to_csv()

    # If still empty → use config default city
    if not cities:
        cities = [cfg["city"]]

    # Validate city names
    valid = []
    for c in cities:
        if validate_city_name(c):
            valid.append(c)
        else:
            print(f"\n❌ Invalid city name: {c}")
            print("Allowed: letters, spaces, hyphens.")
            print("Example: Delhi, New York, Pune-East")
            exit(1)

    return valid




# --------------------------- PER-CITY PROCESSING ---------------------------

def process_city(city, base_lat, base_lon, use_cache, alert_temp, args):
    print(f"\n{Fore.BLUE}{Style.BRIGHT}====== {city.upper()} ======{Style.RESET_ALL}")
    logging.info(f"Processing city: {city}")

    # Coordinates
    lat, lon = get_coords_for_city(city, base_lat, base_lon)
    logging.info(f"Coordinates for {city}: {lat}, {lon}")

    # Map support
    if args.map:
        open_map(lat, lon)

    weather = None
    previous_temp = None

    # Load cache
    if use_cache:
        cached, prev_temp = load_cache(city)
        if cached:
            weather = cached
            previous_temp = prev_temp
            print(f"{Fore.GREEN}{Style.BRIGHT}Using Cached Weather...{Style.RESET_ALL}")

    # Fetch fresh if needed
    if weather is None:
        logging.info(f"Fetching new weather data for {city}")
        weather = fetch_weather(lat, lon)

        if weather:
            print(f"{Fore.CYAN}{Style.BRIGHT}Fetched New Weather Data...{Style.RESET_ALL}")
            save_cache(city, weather)
        else:
            logging.error(f"Failed to fetch weather for {city}")
            print(f"{Fore.RED}❌ Failed to fetch weather for {city}.{Style.RESET_ALL}")
            return

    # Weather formatted output
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}🌤 Weather Details:{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}• Temperature: {Fore.MAGENTA}{weather['temperature']}°C{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}• Wind Speed: {Fore.CYAN}{weather['windspeed']} km/h{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}• Wind Direction: {Fore.BLUE}{weather['winddirection']}°{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}• Time: {Fore.WHITE}{weather['time']}{Style.RESET_ALL}")

    # Temperature Trend
    if previous_temp is not None:
        diff = weather["temperature"] - previous_temp

        if diff > 0:
            print(f"{Fore.YELLOW}📈 Temperature Rising (+{diff:.1f}°C){Style.RESET_ALL}")
        elif diff < 0:
            print(f"{Fore.CYAN}📉 Temperature Dropping ({diff:.1f}°C){Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}➖ Temperature Stable{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}ℹ No previous temperature to compare.{Style.RESET_ALL}")

    # Alerts
    if check_alert(weather, alert_temp):
        print(f"{Fore.RED}{Style.BRIGHT}⚠ ALERT ACTIVE FOR {city}!{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✅ No alert for {city}.{Style.RESET_ALL}")


# --------------------------- MAIN ENTRY ---------------------------

def main():
    args = get_args()
    cfg = load_config(args.config)

    setup_logging(args.log_level or cfg["log_level"])

    use_cache = args.use_cache or cfg["use_cache"]
    alert_temp = args.alert_temp or cfg["alert_temp"]

    base_lat = args.lat or cfg["lat"]
    base_lon = args.lon or cfg["lon"]

    cities = build_city_list(args, cfg)

    logging.info(f"Cities to process: {cities}")
    logging.info(f"Caching enabled: {use_cache}")
    logging.info(f"Alert temperature threshold: {alert_temp}°C")

    # concurrency
    with ThreadPoolExecutor(max_workers=len(cities)) as executor:
        futures = [
            executor.submit(
                process_city,
                city,
                base_lat,
                base_lon,
                use_cache,
                alert_temp,
                args
            )
            for city in cities
        ]

        for _ in as_completed(futures):
            pass

    if args.show_cache:
        print_cache_as_table()

    logging.info("All cities processed.")
    print(f"{Fore.GREEN}✅ All cities processed.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
