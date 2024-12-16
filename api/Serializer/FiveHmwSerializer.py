from rest_framework import serializers

class FiveHmwSerializer(serializers.Serializer):
    root_problem = serializers.CharField()