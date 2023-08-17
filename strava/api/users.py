from django.views.decorators.csrf import csrf_exempt
from strava.api.helpers.request import request_handler
from strava.api.helpers.handlers import generate_handlers


@csrf_exempt
def users(request):
    c, r, u, d = generate_handlers(
        "users", ["username", "access_token", "refresh_token"], ["id"]
    )
    return request_handler(c, r, u, d)(request)
