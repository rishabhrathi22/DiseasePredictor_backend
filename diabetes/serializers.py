from rest_framework import serializers

class FourInputDiabetes(serializers.Serializer):
    glucose = serializers.IntegerField(min_value = 0)
    bmi = serializers.FloatField(min_value = 0)
    dp_function = serializers.FloatField(min_value = 0)
    age = serializers.IntegerField(min_value = 0)

class EightInputDiabetes(serializers.Serializer):
    pregnancies = serializers.IntegerField(min_value = 0)
    glucose = serializers.IntegerField(min_value = 0)
    bp = serializers.IntegerField(min_value = 0)
    skin_thickness = serializers.IntegerField(min_value = 0)
    insulin = serializers.IntegerField(min_value = 0)
    bmi = serializers.FloatField(min_value = 0)
    dp_function = serializers.FloatField(min_value = 0)
    age = serializers.IntegerField(min_value = 0)