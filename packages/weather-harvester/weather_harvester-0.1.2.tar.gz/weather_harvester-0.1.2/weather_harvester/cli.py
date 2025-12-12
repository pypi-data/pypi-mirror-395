import argparse

def get_args(arg_list=None):
    parser = argparse.ArgumentParser(description="Weather Harvester CLI")

    # -------------------- POSITIONAL CITY --------------------
    parser.add_argument(
        "positional_city",
        nargs="*",
        help="City name(s) provided without flags"
    )

    # -------------------- CITY FLAGS --------------------
    parser.add_argument(
        "-c", "--city",
        dest="cities",
        action="append",
        help="City name (can be used multiple times: -c Delhi -c Pune)"
    )

    parser.add_argument(
        "-C", "--cities",
        type=str,
        help="Comma-separated list of cities: --cities Delhi,Mumbai"
    )

    # -------------------- COORDINATES --------------------
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude override (used if city has no predefined coordinates)"
    )

    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude override (used if city has no predefined coordinates)"
    )

    # -------------------- CACHE OPTIONS --------------------
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Use cached weather data if available"
    )

    parser.add_argument(
        "--show-cache",
        action="store_true",
        help="Display cached weather data as a table"
    )

    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Export cached weather data to CSV"
    )

    # -------------------- LOGGING & CONFIG --------------------
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config/config.ini",
        help="Path to configuration file"
    )

    # -------------------- ALERT OPTIONS --------------------
    parser.add_argument(
        "--alert-temp",
        type=float,
        help="Trigger alert if temperature exceeds this threshold (°C)"
    )

    parser.add_argument(
        "--alert-low",
        type=float,
        help="Trigger alert if temperature drops below this threshold (°C)"
    )

    # -------------------- MISCELLANEOUS --------------------
    parser.add_argument(
        "--map",
        action="store_true",
        help="Open city location in Google Maps"
    )

    # -------------------- TESTING SUPPORT --------------------
    if arg_list is not None:
        return parser.parse_args(arg_list)

    return parser.parse_args()
