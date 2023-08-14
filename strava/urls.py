from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name=""),
    path("ping", views.ping, name="ping"),
    path("webhook", views.webhook, name="webhook"),
    path("users", views.users, name="users"),
]
