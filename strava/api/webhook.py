from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from strava.api.helpers.request import request_handler
from strava.api.helpers.request import restricted
from strava.api.auth import verified_tokens
from strava.api.helpers.request import request_handler, restricted, get_body
from django.http import JsonResponse
from strava.api.activities import (
    get_activity_strava,
    update_activity_description,
    generate_activity_description,
)
import os
import requests


@csrf_exempt
def webhook(request) -> JsonResponse:
    def read(request):
        return handle_webhook_subscribe(request, os.environ.get("VERIFY_TOKEN"))

    def create(request):
        send_website_update_webhook()
        return JsonResponse({"message": "Webhook received"}, status=200)

    return request_handler(create, read, restricted, restricted)(request)


def handle_activity_webhook(user_id, activity_id):
    send_website_update_webhook()
    access_token, _ = verified_tokens(user_id)
    activity = get_activity_strava(activity_id, access_token)
    description = generate_activity_description(activity)
    res = update_activity_description(activity_id, description, access_token)
    return res, description


def handle_webhook_subscribe(request, secret_token) -> JsonResponse:
    mode, token, challenge = (
        request.GET.get("hub.mode"),
        request.GET.get("hub.verify_token"),
        request.GET.get("hub.challenge"),
    )

    is_invalid = not mode or not token or not challenge
    is_subscribable = mode == "subscribe" and token == secret_token

    if is_invalid:
        return JsonResponse({"error": "Bad request"}, status=400)
    if is_subscribable:
        return JsonResponse({"hub.challenge": challenge})

    return JsonResponse({"error": "Forbidden"}, status=403)

def send_website_update_webhook():
    url = "https://api.github.com/repos/johnsfarrell/site/dispatches"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}",
    }
    data = {
        "event_type": "Strava Activity Upload",
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 204:
        print("Webhook dispatched successfully.")
    else:
        print(f"Failed to dispatch webhook. Status code: {response.status_code}")
        print(f"Response: {response.text}")