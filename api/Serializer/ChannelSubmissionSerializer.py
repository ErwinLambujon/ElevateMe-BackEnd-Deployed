from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.Model.ChannelMember import ChannelMember
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser
from api.Model.RoomChannel import RoomChannel


class ChannelSubmissionSerializer(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()

    class Meta:
        model = ChannelSubmission
        fields = '__all__'
        read_only_fields = ['date_submitted']

    def get_member_name(self, obj):
        return f"{obj.member_id.first_name} {obj.member_id.last_name}"

    def validate(self, attrs):
        channel_id = attrs.get('channel_id')
        member_id = attrs.get('member_id')

        if not channel_id or not member_id:
            raise serializers.ValidationError({
                "non_field_errors": "Both channel_id and member_id are required"
            })

        try:
            channel = RoomChannel.objects.get(id=channel_id.id)
        except RoomChannel.DoesNotExist:
            raise serializers.ValidationError({
                "channel_id": f"Channel with id {channel_id.id} does not exist"
            })

        try:
            member = CustomUser.objects.get(id=member_id.id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({
                "member_id": f"User with id {member_id.id} does not exist"
            })

        if not ChannelMember.objects.filter(member_id=member.id, channel_id=channel.id).exists():
            raise serializers.ValidationError({
                "non_field_errors": f"Member with id {member.id} does not exist in channel with id {channel.id}"
            })

        if ChannelSubmission.objects.filter(channel_id=channel.id, member_id=member.id).exists():
            raise serializers.ValidationError({
                "non_field_errors": f"Member with id {member.id} has already submitted in channel with id {channel.id}"
            })

        return attrs