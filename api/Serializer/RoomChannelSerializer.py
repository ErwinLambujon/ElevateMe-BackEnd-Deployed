from rest_framework import serializers

from api.Model.RoomChannel import RoomChannel
from api.Serializer.ChannelMemberSerializer import ChannelMemberSerializer


class RoomChannelSerializer(serializers.ModelSerializer):
    new_channel_member_emails = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        allow_empty=True,
        write_only=True
    )

    class Meta:
        model = RoomChannel
        fields = '__all__'


