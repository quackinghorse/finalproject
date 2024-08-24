from rest_framework import serializers
from .models import WebcamImage

class WebcamImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebcamImage
        fields = '__all__'
from .models import GasSensor, Position, Detection

class GasSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasSensor
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'

