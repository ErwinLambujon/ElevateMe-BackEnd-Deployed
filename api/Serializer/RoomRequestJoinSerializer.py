from rest_framework import serializers

from api.Model.RoomRequestJoin import RoomRequestJoin


class RoomRequestJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRequestJoin
        fields = '__all__'