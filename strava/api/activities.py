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
    adjust_pace,
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
    average_speed = activity["average_speed"]
    start_date = activity["start_date"]
    start_latlng = activity["start_latlng"]
    lat, lng = start_latlng[0], start_latlng[1]
    total_elevation_gain = activity["total_elevation_gain"]
    elev_high = activity["elev_high"]
    (
        temperature,
        precipitation,
        wind_speed,
        humidity,
        dew_point,
    ) = get_weather(start_date, lat, lng)
    heat_index = calculate_heat_index(temperature, humidity)
    real_pace = adjust_pace(average_speed, temperature, humidity, wind_speed)
    pace_final = km_per_min_to_mile_per_min(real_pace)
    return f"PACE: {pace_final}\naverage speed: {average_speed}\nstart date: {start_date}\nstart latlng: {start_latlng}\ntotal elevation gain: {total_elevation_gain}\nelev high: {elev_high}\ntemperature: {temperature}\nprecipitation: {precipitation}\nwind speed: {wind_speed}\nhumidity: {humidity}\ndew point: {dew_point}\nheat index: {heat_index}\nreal_pace: {real_pace}"


def km_per_min_to_mile_per_min(pace_km):
    conversion_factor = 1.60934
    pace_mile = pace_km * conversion_factor

    minutes = int(pace_mile)
    seconds = int((pace_mile - minutes) * 60)

    return f"{minutes}:{seconds:02}"
