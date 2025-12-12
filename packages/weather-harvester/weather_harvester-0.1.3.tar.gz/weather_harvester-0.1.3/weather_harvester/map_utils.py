# map_utils.py
import folium
import webbrowser
import os


def open_weather_map(city: str, lat: float, lon: float, temp: float, windspeed: float):
    """
    Create and open an interactive weather map for the given city.
    """

    # Choose marker color based on temperature
    if temp <= 5:
        color = "blue"
    elif temp <= 20:
        color = "green"
    elif temp <= 35:
        color = "orange"
    else:
        color = "red"

    # Base map
    m = folium.Map(location=[lat, lon], zoom_start=11, tiles="OpenStreetMap")

    popup_html = f"""
    <b>{city.title()}</b><br>
    Temperature: {temp}°C<br>
    Wind speed: {windspeed} km/h<br>
    """

    folium.Marker(
        location=[lat, lon],
        popup=popup_html,
        tooltip=f"{city.title()} Weather",
        icon=folium.Icon(color=color, icon="cloud")
    ).add_to(m)

    # Also add a circle to show area around the city
    folium.Circle(
        radius=5000,
        location=[lat, lon],
        color=color,
        fill=True,
        fill_opacity=0.15,
    ).add_to(m)

    # Save file and open it
    safe_name = city.replace(" ", "_").lower()
    file_name = f"{safe_name}_weather_map.html"
    m.save(file_name)

    full_path = os.path.realpath(file_name)
    print(f"🗺 Opening weather map for {city}: {full_path}")
    webbrowser.open(f"file://{full_path}")