
from rest_framework import serializers
from ..Model.ProblemStatement import TwoVennProblemStatementModel, ThreeVennProblemStatementModel
from ..Serializer.VennSerializer import TwoVennSerializer, ThreeVennSerializer

class TwoVennProblemStatementSerializer(serializers.ModelSerializer):
    venn = TwoVennSerializer()  # Remove read_only=True

    class Meta:
        model = TwoVennProblemStatementModel
        fields = '__all__'


    def create(self, validated_data):
        venn = validated_data.pop("venn", None)
        user = validated_data.pop('user', None)

        if venn:
            two_venn_serializer = TwoVennSerializer(data=venn)
            if two_venn_serializer.is_valid():
                venn_instance = two_venn_serializer.save(user=user)
                problem_statement = TwoVennProblemStatementModel.objects.create(venn=venn_instance, **validated_data, user=user)
                return problem_statement
        else:
            raise serializers.ValidationError({"error": "Cannot save a problem statement without venn diagram."})

    def update(self, instance, validated_data):
        venn_data = validated_data.pop('venn', None)
        user = validated_data.pop('user', None)

        if venn_data:
            venn_instance = instance.venn
            venn_serializer = TwoVennSerializer(venn_instance, data=venn_data)
            if venn_serializer.is_valid():
                venn_serializer.save()

        instance.statement = validated_data.get('statement', instance.statement)
        instance.user = user or instance.user
        instance.save()
        return instance


class ThreeProblemStatementSerializer(serializers.ModelSerializer):
    venn = ThreeVennSerializer()

    class Meta:
        model = ThreeVennProblemStatementModel
        fields = '__all__'

    def create(self, validated_data):
        venn = validated_data.pop("venn", None)
        user = validated_data.pop("user", None)
        if venn:
            three_venn_serializer = ThreeVennSerializer(data=venn)
            if three_venn_serializer.is_valid():
                venn = three_venn_serializer.save(user=user)
                problem_statement = ThreeVennProblemStatementModel.objects.create(venn=venn, **validated_data, user=user)
                return problem_statement
        else:
            raise serializers.ValidationError({"error": "Cannot save a problem statement without venn diagram."})

    def update(self, instance, validated_data):
        venn_data = validated_data.pop('venn', None)
        user = validated_data.pop('user', None)
        # print(validated_data)


        if venn_data:
            # So if we passed a data venn it will go here.
            venn_instance = instance.venn
            venn_serializer = TwoVennSerializer(venn_instance, data=venn_data)
            if venn_serializer.is_valid():
                venn_serializer.save()
        instance.statement = validated_data.get('statement', instance.statement)
        instance.user = user or instance.user
        instance.save()
        return instance
