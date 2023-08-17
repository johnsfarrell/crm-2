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

    body = lambda request: json.loads(request.body.decode("utf-8"))

    return lambda request: CRUD[request.method](body(request))
