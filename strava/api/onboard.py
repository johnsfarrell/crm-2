from django.views.decorators.csrf import csrf_exempt
import requests
from django.shortcuts import render
from strava.api.helpers.crud import _create
from strava.src.constants import STRAVA_AUTH_URL, CLIENT_ID, CLIENT_SECRET


@csrf_exempt
def onboard(request):
    if request.method != "GET":
        return render(request, "onboard.html", {"status": "", "username": ""})

    code = request.GET.get("code", None)
    url = f"{STRAVA_AUTH_URL}?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={code}&grant_type=authorization_code"
    res = requests.post(url)

    if not res.status_code in [200, 201]:
        return render(
            request,
            "onboard.html",
            {"status": "error - could not validate"},
        )

    res_json = res.json()
    user_data = _create(
        "users",
        {
            "id": res_json["athlete"]["id"],
            "username": res_json["athlete"]["username"],
            "access_token": res_json["access_token"],
            "refresh_token": res_json["refresh_token"],
        },
    )

    return render(
        request,
        "onboard.html",
        {
            "status": f"success - {res_json['athlete']['username']}"
            if user_data
            else "error",
        },
    )
