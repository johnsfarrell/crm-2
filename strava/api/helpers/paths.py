from django.urls import path


def generate_path(name, method):
    return path(name, method, name=name)
