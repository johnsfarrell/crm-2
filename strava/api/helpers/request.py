from django.http import JsonResponse
import json


def restricted(request):
    return JsonResponse({"requesterrored": [request]}, status=405)


def request_handler(create, read, update, delete):
    CRUD = {
        "POST": create,
        "GET": read,
        "PUT": update,
        "DELETE": delete,
    }

    return lambda request: CRUD[request.method](request)


def get_body(request):
    return json.loads(request.body.decode("utf-8"))
