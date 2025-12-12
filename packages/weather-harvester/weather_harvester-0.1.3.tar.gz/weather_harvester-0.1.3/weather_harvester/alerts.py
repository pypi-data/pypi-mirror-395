import logging
import platform
from colorama import Fore, Style, init
from weather_harvester.turtle_alert import turtle_clean_skull_alert  # from file 1

init(autoreset=True)


def check_alert(weather: dict, alert_temp: float):
    if not weather or "temperature" not in weather:
        logging.warning("Weather data missing for alert check")
        return False

    temp = weather["temperature"]

    if temp >= alert_temp:
        logging.warning(
            f"ALERT! Temperature {temp}°C exceeded threshold {alert_temp}°C"
        )
        print(f"\n{Fore.RED}🔥🔥🔥 TEMPERATURE ALERT 🔥🔥🔥")
        print(f"{Fore.RED}Current temperature: {temp}°C (Threshold: {alert_temp}°C)")

        play_alert_sound()
        turtle_clean_skull_alert()  # from file 1

        return True  # alert happened

    else:
        logging.info(
            f"No alert. Temperature {temp}°C is below threshold {alert_temp}°C"
        )
        return False  # no alert


def play_alert_sound():
    os_name = platform.system()

    try:
        if os_name == "Windows":
            import winsound

            # Emergency pattern (from file 1)
            for _ in range(10):
                winsound.Beep(1500, 150)
                winsound.Beep(1000, 150)

        elif os_name == "Darwin":
            import os
            os.system("say 'Emergency alert'")  # file 1 wording

        else:
            # Linux fallback (beep multiple times)
            for _ in range(10):
                print("\a")

    except Exception as e:
        logging.error(f"Failed to play sound alert: {e}")


def detect_trend(prev_temp, new_temp):
    """Returns 'rising', 'dropping', or 'stable'."""
    if new_temp > prev_temp:
        return "rising"
    elif new_temp < prev_temp:
        return "dropping"
    else:
        return "stable"
