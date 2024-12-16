from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomMember import RoomMember


class RoomSerializer(serializers.ModelSerializer):
    new_room_member_emails = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Room
        fields = '__all__'

    # def create(self, validated_data):
    #     members_data = validated_data.pop('members', [])
    #
    #     room = Room.objects.create(**validated_data)
    #
    #     for email in members_data:
    #
    #         try:
    #             user = CustomUser.objects.get(email=email)
    #         except CustomUser.DoesNotExist:
    #             raise serializers.ValidationError(f"User with email {email} does not exist.")
    #
    #         room_member_data = {
    #             'room': room.pk,
    #             'member_id': user.pk
    #         }
    #
    #         room_member_serializer = RoomMemberSerializer(data=room_member_data)
    #         if room_member_serializer.is_valid():
    #             room_member_serializer.save()
    #         else:
    #             raise serializers.ValidationError(room_member_serializer.errors)
    #
    #     return room


class RoomJoinSerializer(serializers.Serializer):
    room_code = serializers.UUIDField()
    member_id = serializers.IntegerField()

    def validate(self, attrs):
        room_code = attrs.get('room_code')
        member_id = attrs.get('member_id')

        if not Room.objects.filter(room_code=room_code).exists():
            raise ValidationError(f"Room with room code {room_code} does not exist")

        if not CustomUser.objects.filter(id=member_id).exists():
            raise ValidationError(f"Member with member_id {member_id} does not exist")

        return attrs


    def save(self, **kwargs):
        room_code = self.validated_data.get('room_code')
        member_id = self.validated_data.get('member_id')

        room = Room.objects.filter(room_code=room_code).first()
        if not room:
            raise serializers.ValidationError(f"Room with room code {room_code} does not exist")

        member = CustomUser.objects.filter(id=member_id).first()
        if not member:
            raise serializers.ValidationError(f"Member with member_id {member_id} does not exist")

        room_member, created = RoomMember.objects.get_or_create(room_id=room, member_id=member)
        if not created:
            raise serializers.ValidationError("This member is already in the room.")

        return {'room_code': room_code, 'member_id': member_id, "message": 'Joined successfully.'}
