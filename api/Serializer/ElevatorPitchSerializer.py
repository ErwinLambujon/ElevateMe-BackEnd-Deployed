from rest_framework import serializers

from api.Serializer.FiveWhySerializer import FiveWhySerializer
from api.Serializer.PotentialRootSerializer import PotentialRootSerializer


class ElevatorPitchSerializer(serializers.Serializer):
    # I want to put the venn serializer here but I am still be needing to get the value

    list_of_hmws = serializers.ListField(child=serializers.CharField())

