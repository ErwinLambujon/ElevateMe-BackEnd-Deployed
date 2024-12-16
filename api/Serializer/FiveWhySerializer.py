from rest_framework import serializers
class FiveWhySerializer(serializers.Serializer):
    ranked_problem = serializers.CharField()