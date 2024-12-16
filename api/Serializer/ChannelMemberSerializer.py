from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.Model.ChannelMember import ChannelMember
from api.Model.CustomUser import CustomUser
from api.Model.RoomChannel import RoomChannel


class ChannelMemberSerializer(serializers.ModelSerializer):
    channel_members = serializers.ListField(
        child=serializers.EmailField(),
        required=False
    )

    class Meta:
        model = ChannelMember
        fields = '__all__'


    def validate(self, attrs):
        channel_id = attrs.get('channel_id')
        member_id = attrs.get('member_id')

        if ChannelMember.objects.filter(channel_id=channel_id, member_id=member_id).exists():
            raise ValidationError(f'This member is already in the channel.')

        return attrs

class ChannelMemberDeletionSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    channel_id = serializers.IntegerField()

    def validate(self, attrs):
        member_id = attrs.get('member_id')
        channel_id = attrs.get('channel_id')

        if not RoomChannel.objects.filter(id=channel_id).exists():
            raise ValidationError(f'Channel with channel_id: {channel_id} does not exists')

        if not CustomUser.objects.filter(id=member_id).exists():
            raise ValidationError(f'Member with member_id: {member_id} does not exists')

        if not ChannelMember.objects.filter(channel_id=channel_id, member_id=member_id).exists():
            raise ValidationError(f'Member with member_id {member_id} is not a member of channel with channel_id {channel_id}')

        return attrs

    def delete(self):
        channel_id = self.validated_data.get('channel_id')
        member_id = self.validated_data.get('member_id')

        room_member = ChannelMember.objects.get(channel_id=channel_id, member_id=member_id)
        room_member.delete()
        return True