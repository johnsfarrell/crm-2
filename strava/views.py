from django.http import HttpResponse
from strava.api.webhook import webhook
from strava.api.users import users
from strava.api.onboard import onboard
from strava.api.activities import activities


def index(request):
    return HttpResponse("", status=200)


def ping(request):
    return HttpResponse("pong", status=200)


VIEWS = {
    "webhook": webhook,
    "users": users,
    "onboard": onboard,
    "activites": activities,
    "ping": ping,
    "": index,
}
