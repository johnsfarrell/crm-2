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
from strava.src.constants import VERIFY_TOKEN


@csrf_exempt
def webhook(request) -> JsonResponse:
    def read(request):
        return handle_webhook_subscribe(request, VERIFY_TOKEN)

    def create(request):
        print("test line 1")
        body = get_body(request)
        print("test line 2")
        object_type, aspect_type = body["object_type"], body["aspect_type"]
        print("test line 3")
        is_activity_creation = object_type == "activity" and aspect_type == "create"
        print("test line 4")
        if not is_activity_creation:
            print("test line 5")
            return JsonResponse({"skip": "yes, not an activity creation"}, status=200)
        print("test line 6")
        user_id, activity_id = body["owner_id"], body["object_id"]
        print("test line 7")
        res, description = handle_activity_webhook(user_id, activity_id)
        print("test line 8")
        if not res.status in ["200", "201", 200, 201]:
            print("test line 9")
            return JsonResponse({"error": f"{res}"}, status=res.status)
        print("test line 10")
        return JsonResponse({"success": f"{description}", "req": res}, status=200)

    return request_handler(create, read, restricted, restricted)(request)


def handle_activity_webhook(user_id, activity_id):
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
