from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uid = serializers.CharField()

class UIDSerializer(serializers.Serializer):
    uid = serializers.CharField()