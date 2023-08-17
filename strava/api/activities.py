from strava.src.constants import STRAVA_URL
import requests
import json
from strava.api.helpers.utils import bearer
from strava.api.helpers.request import request_handler
from strava.api.helpers.handlers import generate_handlers
from strava.api.helpers.crud import _create


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
        return {"status": res.status_code, "message": res.text}
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
    return "HELLO... " + json.dumps(activity, indent=4, sort_keys=True)
