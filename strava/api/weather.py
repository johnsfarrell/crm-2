import json
import requests
import os

WEATHER_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata"


def get_weather(time, lat, lng):
    location = f"{lat},{lng}"
    url = f"{WEATHER_URL}/history?aggregateHours=1&startDateTime={time}&endDateTime={time}&location={location}&unitGroup=us&key={os.environ.get('VISUAL_CROSSING_API_KEY')}&contentType=json"
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
    precipitation,
):
    # Adjust for temperature
    if temperature > 75:
        speed *= 1.03
    elif temperature < 40:
        speed *= 1.02

    # Adjust for humidity
    if humidity > 85:
        speed *= 1.05
    elif humidity > 70:
        speed *= 1.02

    # Adjust for dew point
    if dew_point > 70:
        speed *= 1.07
    elif dew_point > 65:
        speed *= 1.04

    # Adjust for wind speed
    if wind_speed > 10:  # If wind is strong and against runner
        speed *= 1.03
    elif wind_speed < -10:  # If wind is strong and aiding runner
        speed *= 0.97

    # Adjust for heat index
    if heat_index > 90:
        speed *= 1.06

    # Adjust for elevation gain
    if elevation_gain > 150:  # Roughly 500 feet
        speed *= 1.05
    elif elevation_gain > 300:  # Roughly 1000 feet
        speed *= 1.10

    # Adjust for high elevation
    if elevation_high > 1500:  # Where noticeable effects start to kick in
        speed *= 1.04
    elif elevation_high > 3000:  # More pronounced effects
        speed *= 1.08

    # Adjust for precipitation
    if precipitation > 0.2:  # Heavy precipitation
        speed *= 1.05
    elif precipitation > 0.1:  # Light precipitation
        speed *= 1.02

    return speed
