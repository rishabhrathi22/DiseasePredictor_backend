from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uid = serializers.CharField(max_length = 200)