from django.forms import model_to_dict
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.response import Response

from api.Model.ChannelMember import ChannelMember
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomChannel import RoomChannel
from api.Model.SubmissionVoting import SubmissionVotingMark
from api.Serializer.ChannelMemberSerializer import ChannelMemberSerializer, ChannelMemberDeletionSerializer
from api.Serializer.ChannelSubmissionSerializer import ChannelSubmissionSerializer
from api.Serializer.RoomChannelSerializer import RoomChannelSerializer


class RoomChannelView(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = RoomChannel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RoomChannelSerializer


    """
        Payload is the request.body from the front-end
        Payload in creating a room channel
        {
            channel_name: string,
            room_id: int,
            channel_members: list[] only members sa room
        }
    """

    def get_serializer_class(self):
        if self.action == "members":
            return ChannelMemberSerializer
        if self.action == "remove_channel_member":
            return ChannelMemberDeletionSerializer
        if self.action == "submit":
            return ChannelSubmissionSerializer
        return RoomChannelSerializer



    def get_object(self):
        if self.action == "members":
            channel = super().get_object()
            return ChannelMember.objects.filter(channel_id=channel.id)
        else:
            channel = super().get_object()
            user = self.request.user

            if not ChannelMember.objects.filter(channel_id=channel.id, member_id=user.id).exists():
                raise PermissionDenied("You are not a member of this channel.")

            return channel

    def create(self, request, *args, **kwargs):
        channel_members = request.data.get('channel_members', [])
        channel_name = request.data.get('channel_name')
        room_id = request.data.get('room_id')

        room = Room.objects.filter(id=room_id).first()

        channel_serializer = self.get_serializer(data={"channel_name": channel_name, "room_id": room.id })
        channel_serializer.is_valid(raise_exception=True)

        user = request.user
        members = [user]

        for email in channel_members:
            try:
                member = CustomUser.objects.get(email=email)
                members.append(member)
            except CustomUser.DoesNotExist:
                raise ValidationError(f'User with email {email} does not exist.')


        channel = channel_serializer.save()

        for member in members:
            channel_member_data = {
                "member_id": member.id,
                "channel_id": channel.id
            }

            channel_member_serializer = ChannelMemberSerializer(data=channel_member_data)
            channel_member_serializer.is_valid(raise_exception=True)
            channel_member_serializer.save()

        return Response(channel_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        channel = self.get_object()
        members_to_be_added = request.data.get('new_channel_member_emails', [])
        room_id = request.data.get('room_id')

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise ValidationError(f"Room with ID: {room_id} does not exist")

        for member_email in members_to_be_added:
            try:
                to_be_added = CustomUser.objects.get(email=member_email)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email: {member_email} does not exist")

            channel_member_data = {
                "room_id": room.id,
                "member_id": to_be_added.id,
                "channel_id": channel.id
            }

            channel_member_serializer = ChannelMemberSerializer(data=channel_member_data)
            channel_member_serializer.is_valid(raise_exception=True)
            channel_member_serializer.save()

        return Response({"message": "Successfully added to the channel"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        room_members = self.get_object()

        serializer = self.get_serializer(room_members, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='members/(?P<member_id>[^/.]+)')
    def remove_channel_member(self, request, pk, member_id):
        serializer = self.get_serializer(data={'channel_id': pk, 'member_id': member_id})
        serializer.is_valid(raise_exception=True)

        try:
            user_submissions = ChannelSubmission.objects.filter(
                member_id=member_id,
                channel_id=pk
            )

            submission_ids = user_submissions.values_list('id', flat=True)

            user_submissions.delete()

            # Delete voting marks received by the user's submissions
            SubmissionVotingMark.objects.filter(submission_id__in=submission_ids).delete()

            # Delete voting marks made by the user in the channel
            SubmissionVotingMark.objects.filter(
                member_id=member_id,
                submission_id__channel_id=pk
            ).delete()

            ChannelMember.objects.filter(channel_id=pk, member_id=member_id).delete()

            return Response(
                {"message": "Member removed from channel and all associated data"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to remove member: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='is-member/(?P<member_id>[^/.]+)')
    def is_user_member(self, request, pk, member_id):
        try:
            is_member = ChannelMember.objects.filter(channel_id=pk, member_id=member_id).exists()
            return Response({"is_member": is_member}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to check membership: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )
