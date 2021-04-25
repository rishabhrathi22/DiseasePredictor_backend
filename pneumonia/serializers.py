from rest_framework import serializers

class PneumoniaSerializer(serializers.Serializer):
    base64Image = serializers.CharField()