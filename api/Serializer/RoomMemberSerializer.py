from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomMember import RoomMember
from api.Serializer.RoomSerializer import RoomSerializer


class RoomMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMember
        fields = '__all__'

    def validate(self, attrs):
        room_id = attrs.get('room_id')
        member_id = attrs.get('member_id')

        if RoomMember.objects.filter(room_id=room_id, member_id=member_id).exists():
            raise ValidationError(f'This member is already in the room.')

        return attrs

class RoomMemberDeletionSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    member_id = serializers.IntegerField()

    def validate(self, attrs):
        room_id = attrs.get('room_id')
        member_id = attrs.get('member_id')

        if not Room.objects.filter(id=room_id).exists():
            raise ValidationError(f'Room with room_id: {room_id} does not exists')

        if not CustomUser.objects.filter(id=member_id).exists():
            raise ValidationError(f'Member with member_id: {member_id} does not exists')

        if not RoomMember.objects.filter(room_id=room_id, member_id=member_id).exists():
            raise ValidationError(f'Member with member_id {member_id} is not a member of room with room_id {room_id}')

        return attrs


    def delete(self):
        room_id = self.validated_data.get('room_id')
        member_id = self.validated_data.get('member_id')

        room_member = RoomMember.objects.get(room_id=room_id, member_id=member_id)
        room_member.delete()
        return True