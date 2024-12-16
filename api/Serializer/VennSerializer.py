from rest_framework import serializers

from ..Model.VennDiagram import TwoVennDiagramModel, ThreeVennDiagramModel

class TwoVennSerializer(serializers.ModelSerializer):
    filter = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = TwoVennDiagramModel
        fields = ['field1', 'field2', 'filter']


    def create(self, validated_data):
        print(validated_data)
        return TwoVennDiagramModel.objects.create(**validated_data)


class ThreeVennSerializer(serializers.ModelSerializer):
    filter = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    class Meta:
        model = ThreeVennDiagramModel
        fields = ['field1', 'field2', 'filter', 'field3']

    def create(self, validated_data):
        return ThreeVennDiagramModel.objects.create(**validated_data)