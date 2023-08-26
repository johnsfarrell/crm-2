import json
import requests

WEATHER_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata"
VISUAL_CROSSING_API_KEY = "EVWNLXNJHRAQ4FUYNM663JMVP"


def get_weather(time, lat, lng):
    location = f"{lat},{lng}"
    url = f"{WEATHER_URL}/history?aggregateHours=1&startDateTime={time}&endDateTime={time}&location={location}&unitGroup=us&key={VISUAL_CROSSING_API_KEY}&contentType=json"
    res = requests.get(url)
    if not res.status_code in [200, 201]:
        return None
    res = res.json()
    data = res["locations"][f"{location}"]["values"][0]
    temp, precip, wspd, humidity, dew = (
        data["temp"],
        data["precip"],
        data["wspd"],
        data["humidity"],
        data["dew"],
    )
    return temp, precip, wspd, humidity, dew


def calculate_heat_index(temp, humidity):
    c = [
        (-42.379),
        (2.04901523),
        (10.14333127),
        (-0.22475541),
        (-0.00683783),
        (-0.05481717),
        (0.00122874),
        (0.00085282),
        (-0.00000199),
    ]

    heat_index = (
        c[0]
        + (c[1] * temp)
        + (c[2] * humidity)
        + (c[3] * temp * humidity)
        + (c[4] * temp**2)
        + (c[5] * humidity**2)
        + (c[6] * temp**2 * humidity)
        + (c[7] * temp * humidity**2)
        + (c[8] * temp**2 * humidity**2)
    )

    return round(heat_index, 2)


def adjust_pace(speed, temperature, humidity, wind_speed):
    """
    Adjust running pace based on weather factors.

    pace_minutes: Actual pace in minutes per mile/km
    pace_seconds: Actual pace in seconds per mile/km (remainder after minutes)
    temperature: Current temperature in °F (could adjust for °C if needed)
    humidity: Current relative humidity (0-100%)
    wind_speed: Current wind speed in mph (could adjust for km/h if needed)

    Returns: Adjusted pace as (minutes, seconds)
    """
    # Adjust pace for temperature
    # Assuming anything above 75°F begins to slow the runner down and anything below 40°F also slows the runner.
    if temperature > 75:
        speed += (temperature - 75) * 0.2
    elif temperature < 40:
        speed += (40 - temperature) * 0.1

    # Adjust pace for humidity
    # Assuming high humidity above 70% slows the runner.
    if humidity > 70:
        speed += (humidity - 70) * 0.1

    # Adjust pace for wind
    # Assuming strong winds above 10 mph slows the runner.
    if wind_speed > 10:
        speed += (wind_speed - 10) * 0.5

    return speed
