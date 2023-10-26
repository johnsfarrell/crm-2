from django.http import JsonResponse
import requests
from strava.src.constants import STRAVA_URL, STRAVA_AUTH_URL
from strava.api.helpers.crud import _read, _update
from strava.api.helpers.utils import bearer
import os


def authorization_code(request):
    code, grant_type = request.GET.get("code"), request.GET.get("grant_type")

    valid_params = code and grant_type == "authorization_code"
    if not valid_params:
        return JsonResponse({"error": "Bad request, invalid params"}, status=400)

    res = requests.post(
        f"{STRAVA_URL}/oath/token?client_id={os.environ.get('CLIENT_ID')}&client_secret={os.environ.get('CLIENT_SECRET')}&code={code}&grant_type={grant_type}"
    )
    res = res.json()

    access_token, refresh_token = res.get("access_token"), res.get("refresh_token")
    id, username = res.get("athlete").get("id"), res.get("athlete").get("username")

    valid_data = refresh_token and access_token and id and username
    if not valid_data:
        return JsonResponse({"error": "Bad request, invalid data"}, status=400)

    res = _update(
        "users",
        id,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "username": username,
        },
    )

    return JsonResponse({"success": "Successfully updated db"}, status=200)


def verified_tokens(user_id):
    access_token, refresh_token = get_tokens(user_id)
    if not is_access_token_valid(user_id):
        access_token, refresh_token = update_tokens(user_id)
    return access_token, refresh_token


def get_tokens(user_id):
    res = _read("users", user_id)
    access_token, refresh_token = res.get("access_token"), res.get("refresh_token")
    return access_token, refresh_token


def is_access_token_valid(user_id):
    access_token, _ = get_tokens(user_id)
    if not access_token:
        return False

    url = f"{STRAVA_URL}/athletes/{user_id}/stats"
    headers = {"Authorization": bearer(access_token)}
    res = requests.get(url, headers=headers)

    return res.status_code in [200, 201, "200", "201"]


def update_tokens(user_id):
    _, refresh_token = get_tokens(user_id)
    res = requests.post(
        f"{STRAVA_AUTH_URL}?client_id={os.environ.get('CLIENT_ID')}&client_secret={os.environ.get('CLIENT_SECRET')}&refresh_token={refresh_token}&grant_type=refresh_token"
    )
    if not res.status_code in [200, 201, "200", "201"]:
        return None, refresh_token

    res = res.json()
    access_token, refresh_token = res.get("access_token"), res.get("refresh_token")

    res = _update(
        "users", user_id, {"access_token": access_token, "refresh_token": refresh_token}
    )

    return access_token if res else None, refresh_token
