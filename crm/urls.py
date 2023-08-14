from django.urls import path, include

urlpatterns = [
    path("strava/", include("strava.urls")),
]
