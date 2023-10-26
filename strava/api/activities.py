from strava.src.constants import STRAVA_URL
import requests
import json
from strava.api.helpers.utils import bearer
from strava.api.helpers.request import request_handler
from strava.api.helpers.handlers import generate_handlers
from strava.api.helpers.crud import _create
from strava.api.weather import (
    get_weather,
    calculate_heat_index,
    adjust_speed,
)


def activities(request):
    c, r, u, d = generate_handlers("activities", ["rawdata"], ["id"])
    return request_handler(c, r, u, d)(request)


def update_activity_description(activity_id, description, token):
    url = f"{STRAVA_URL}/activities/{activity_id}"
    payload = {"description": description}
    headers = {"Authorization": bearer(token)}
    response = requests.put(url, json=payload, headers=headers)
    return response


def get_activity_strava(activity_id, token):
    url = f"{STRAVA_URL}/activities/{activity_id}?include_all_efforts=true"
    headers = {"Authorization": bearer(token)}
    res = requests.get(url, headers=headers)
    if not res.status_code in [200, 201]:
        return res
    res = res.json()
    _create(
        "activities",
        {
            "user_id": res["athlete"]["id"],
            "rawdata": json.dumps(res, indent=4, sort_keys=True),
        },
    )
    return res


def generate_activity_description(activity):
    old_description = activity["description"]
    new_description = generate_description(activity)
    return (
        f"{old_description}\n-\n{new_description}"
        if old_description and len(old_description) > 0
        else new_description
    )


def generate_description(activity):
    # extract data from activity
    average_speed = activity["average_speed"]  # meters per second
    start_date = activity["start_date"]
    start_latlng = activity["start_latlng"]
    lat, lng = start_latlng[0], start_latlng[1]
    total_elevation_gain = activity["total_elevation_gain"]
    elev_high = activity["elev_high"]

    # get weather data
    (
        temperature,
        precipitation,
        wind_speed,
        humidity,
        dew_point,
    ) = get_weather(start_date, lat, lng)

    #
    heat_index = calculate_heat_index(temperature, humidity)
    adjusted_speed = adjust_speed(
        average_speed, temperature, humidity, dew_point, wind_speed, heat_index, total_elevation_gain, elev_high
    )
    original_pace = mps_to_min_per_mile(average_speed)
    adjusted_pace = mps_to_min_per_mile(adjusted_speed)

    return f"{adjusted_pace} ☁️\n\n\n\
    
            DEBUG:\n\
            Temperature:               {temperature} ℉\n\
            Precipitation:             {precipitation} in\n\
            Wind Speed:                {wind_speed} mph\n\
            Humidity:                  {humidity} %\n\
            Dew Point:                 {dew_point} ℉\n\
            Heat Index:                {heat_index}\n\
            Elevation Gain:            {total_elevation_gain} m\n\
            Elevation High:            {elev_high} m\n\
            Original Pace:             {original_pace}\n\
            "


def mps_to_min_per_mile(speed_mps):
    # Convert m/s to min/mile
    total_seconds_per_mile = 1609.34 / speed_mps
    minutes = int(total_seconds_per_mile // 60)
    seconds = int(total_seconds_per_mile % 60)

    # Format and return the result as MM:SS
    return f"{minutes:02d}:{seconds:02d}"
