from rest_framework import serializers

class PotentialRootSerializer(serializers.Serializer):
    list_of_whys = serializers.ListField(
        child=serializers.CharField()
    )

    def validate(self, data):
        list_of_whys = data.get('list_of_whys')
        if not list_of_whys:
            raise serializers.ValidationError({"error": "Cannot take an empty list of whys."})
        return data