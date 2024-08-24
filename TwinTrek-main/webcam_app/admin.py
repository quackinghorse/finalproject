from django.contrib import admin
from .models import WebcamImage

@admin.register(WebcamImage)
class WebcamImageAdmin(admin.ModelAdmin):
    list_display=['id', 'image', 'timestamp']
# Register your models here.
