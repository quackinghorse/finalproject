from django.db import models

class WebcamImage(models.Model):
    image = models.ImageField(upload_to='webcam_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
from django.db import models

class GasSensor(models.Model):
    gas_value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Detection(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    time = models.DateTimeField()

