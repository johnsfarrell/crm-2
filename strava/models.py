from django.db import models


class Athlete(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)


class Activity(models.Model):
    id = models.BigIntegerField(primary_key=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    raw_data = models.JSONField()
