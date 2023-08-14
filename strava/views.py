from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from crm.settings import db
from strava.crud import _read, _update, _delete, _create


def index(request):
    return HttpResponse("", status=200)


def ping(request):
    return HttpResponse("pong", status=200)


@csrf_exempt
def webhook(request):
    VERIFY_TOKEN = "STRAVA"

    if request.method == "GET":
        return handle_webhook_get(request, VERIFY_TOKEN)
    elif request.method == "POST":
        return JsonResponse({"message": "Received POST request"}, status=200)
    else:
        return JsonResponse({}, status=405)  # Method Not Allowed


def handle_webhook_get(request, VERIFY_TOKEN: str) -> JsonResponse:
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return JsonResponse({"hub.challenge": challenge})
        else:
            return JsonResponse({"error": "Forbidden"}, status=403)
    else:
        return JsonResponse({"error": "Bad request"}, status=400)


@csrf_exempt
def users(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "No body provided"}, status=400)

    CRUD = {
        "GET": handle_users_get,
        "PUT": handle_users_put,
        "POST": handle_users_post,
        "DELETE": handle_users_delete,
    }

    if request.method not in CRUD:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    return CRUD[request.method](body)


def handle_users_get(body) -> JsonResponse:
    if "id" not in body:
        users = db.child("users").get()
        return JsonResponse(users.val() or {}, status=200)

    res = _read("users", body["id"])
    if not res:
        return JsonResponse({"error": "Failed to get user"}, status=400)
    return JsonResponse(res, status=200)


def handle_users_put(body) -> JsonResponse:
    res = _update(
        "users",
        body["id"],
        {
            "user": body["username"],
            "access_token": body["access_token"],
            "refresh_token": body["refresh_token"],
        },
    )
    return JsonResponse(
        {"message": "Successfully updated user" if res else "Failed to update user"},
        status=200 if res else 400,
    )


def handle_users_post(body) -> JsonResponse:
    res = _create(
        "users",
        {
            "username": body["username"],
            "access_token": body["access_token"],
            "refresh_token": body["refresh_token"],
        },
    )
    return JsonResponse(
        {"message": "Successfully added user" if res else "Failed to add user"},
        status=200 if res else 400,
    )


def handle_users_delete(body) -> JsonResponse:
    res = _delete("users", body["id"])
    return JsonResponse(
        {"message": "Successfully deleted user" if res else "Failed to delete user"},
        status=200 if res else 400,
    )
