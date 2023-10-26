import json
import requests
from strava.src.constants import VISUAL_CROSSING_API_KEY

WEATHER_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata"


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


def adjust_speed(
    speed,
    temperature,
    humidity,
    dew_point,
    wind_speed,
    heat_index,
    elevation_gain,
    elevation_high,
):
    # Adjust for temperature
    if temperature > 75:
        speed *= 0.97
    elif temperature < 40:
        speed *= 0.98

    # Adjust for humidity
    if humidity > 85:
        speed *= 0.95
    elif humidity > 70:
        speed *= 0.98

    # Adjust for dew point
    if dew_point > 70:
        speed *= 0.93
    elif dew_point > 65:
        speed *= 0.96

    # Adjust for wind speed
    if wind_speed > 10:  # If wind is strong and against runner
        speed *= 0.97
    elif wind_speed < -10:  # If wind is strong and aiding runner
        speed *= 1.03

    # Adjust for heat index
    if heat_index > 90:
        speed *= 0.94

    # Adjust for elevation gain
    if elevation_gain > 150:  # Roughly 500 feet
        speed *= 0.95
    elif elevation_gain > 300:  # Roughly 1000 feet
        speed *= 0.90

    # Adjust for high elevation
    if elevation_high > 1500:  # Where noticeable effects start to kick in
        speed *= 0.96
    elif elevation_high > 3000:  # More pronounced effects
        speed *= 0.92

    return speed
