from django.forms import model_to_dict
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from api.Model.ChannelMember import ChannelMember
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser
from api.Model.Room import Room
from api.Model.RoomChannel import RoomChannel
from api.Model.RoomMember import RoomMember
from api.Model.RoomRequestJoin import RoomRequestJoin
from api.Model.SubmissionVoting import SubmissionVotingMark
from api.Serializer.RoomChannelSerializer import RoomChannelSerializer
from api.Serializer.RoomMemberSerializer import RoomMemberSerializer, RoomMemberDeletionSerializer
from api.Serializer.RoomRequestJoinSerializer import RoomRequestJoinSerializer
from api.Serializer.RoomSerializer import RoomSerializer, RoomJoinSerializer

class RoomView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if (self.action == "members" or
            self.action == "auth_rooms"):
            return RoomMemberSerializer
        elif self.action == "channels":
            return RoomChannelSerializer
        elif self.action == "remove_room_member":
            return RoomMemberDeletionSerializer
        elif self.action == "join":
            return RoomJoinSerializer
        elif self.action == "get_applicants":
            return RoomRequestJoinSerializer
        return RoomSerializer
    def get_room_members(self, room):
        return RoomMember.objects.filter(room_id=room.id)

    def get_room_applicants(self, room):
        return RoomRequestJoin.objects.filter(status='pending', room_id=room.id)

    def create(self, request, *args, **kwargs):
        """
            Payload to create a room
            {
                members: list[]
                room_name: string,
            }
        """
        members_data = request.data.get('new_room_member_emails', [])
        room_name = request.data.get('room_name')

        room_owner = CustomUser.objects.filter(email=request.user).first()

        room_serializer = self.get_serializer(data={"room_name": room_name, "room_owner_id": room_owner.id})
        room_serializer.is_valid(raise_exception=True)

        users = []
        users.append(room_owner)
        for email in members_data:
            try:
                user = CustomUser.objects.get(email=email)
                users.append(user)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email {email} does not exist.")

        room = room_serializer.save()

        for user in users:
            room_member_data = {
                'room_id': room.pk,
                'member_id': user.pk
            }

            room_member_serializer = RoomMemberSerializer(data=room_member_data)
            room_member_serializer.is_valid(raise_exception=True)
            room_member_serializer.save()

        return Response(room_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        members_to_be_added = request.data.get('new_room_members', [])

        print(model_to_dict(room))
        for member_email in members_to_be_added:
            try:
                to_be_added = CustomUser.objects.get(email=member_email)
            except CustomUser.DoesNotExist:
                raise ValidationError(f"User with email: {member_email} does not exist")

            print(model_to_dict(to_be_added))

            room_member_data = {
                "room_id": room.id,
                "member_id": to_be_added.id
            }

            room_member_serializer = RoomMemberSerializer(data=room_member_data)
            room_member_serializer.is_valid(raise_exception=True)
            room_member_serializer.save()

        return Response({"message": "Successfully added to the room"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        room = self.get_object()
        room_members = self.get_room_members(room)
        serializer = RoomMemberSerializer(room_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def channels(self, request, pk):
        user = request.user

        channels = RoomChannel.objects.filter(
            room_id=pk,
            channelmember__member_id=user.id
        ).distinct()

        serializer = self.get_serializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='members/(?P<member_id>[^/.]+)')
    def remove_room_member(self, request, pk, member_id):
        serializer = self.get_serializer(data={'room_id': pk, 'member_id': member_id})
        serializer.is_valid(raise_exception=True)

        try:
            room_channels = RoomChannel.objects.filter(room_id=pk)
            channel_ids = room_channels.values_list('id', flat=True)

            ChannelMember.objects.filter(channel_id__in=channel_ids, member_id=member_id).delete()
            RoomRequestJoin.objects.filter(room_id=pk, user_id=member_id).update(status='removed')

            member_submissions = ChannelSubmission.objects.filter(
                member_id=member_id,
                channel_id__in=channel_ids
            )

            submission_ids = member_submissions.values_list('id', flat=True)
            member_submissions.delete()

            SubmissionVotingMark.objects.filter(submission_id__in=submission_ids).delete()
            SubmissionVotingMark.objects.filter(
                member_id=member_id,
                submission_id__channel_id__in=channel_ids
            ).delete()
            serializer.delete()

            return Response(
                {"message": "Member removed from room and all associated data"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to remove member: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=['post'])
    def join(self, request):
        room_code = request.data.get('room_code')
        member_id = request.user

        # Validate room and user existence
        try:
            room = Room.objects.get(room_code=room_code)
            user = CustomUser.objects.get(id=member_id.id)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if RoomRequestJoin.can_create_request(user=user, room=room):
            join_request = RoomRequestJoin.objects.create(
                user=user,
                room=room,
                status='pending'
            )
            return Response(
                {"message": "Join request created successfully.", "request_id": join_request.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "You already have an active or approved request for this room."},
                status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=True, methods=['post'])
    def manage_request(self, request, pk=None):
        action_type = request.data.get('action')
        request_id = request.data.get('request_id')

        if not action_type:
            return Response(
                {"error": "Action type is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            join_request = RoomRequestJoin.objects.get(
                id=request_id,
                room_id=pk,
                status='pending'
            )
        except RoomRequestJoin.DoesNotExist:
            return Response(
                {"error": "Active join request not found."},
                status=status.HTTP_404_NOT_FOUND
            )


        user = CustomUser.objects.filter(id=join_request.user_id).first()

        if not user:
            raise ValidationError("User not found.")

        if action_type == "accept":
            join_request.status = 'approved'
            join_request.save()

            RoomMember.objects.create(
                room_id_id=pk,
                member_id=user
            )

            return Response(
                {"message": "Join request approved and member added."},
                status=status.HTTP_200_OK
            )

        elif action_type == "reject":
            join_request.status = 'rejected'
            join_request.save()
            return Response(
                {"message": "Join request rejected."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": f"Action '{action_type}' is not supported."},
            status=status.HTTP_400_BAD_REQUEST
        )
    @action(detail=True, methods=['get'])
    def applicants(self, request, pk):
        room = self.get_object()
        room_members = self.get_room_applicants(room)
        serializer = RoomRequestJoinSerializer(room_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def auth_rooms(self, request):
        user = request.user

        room_members = RoomMember.objects.filter(member_id=user.id)

        room_member_serializer = RoomMemberSerializer(room_members, many=True)

        room_ids = set()

        for room_member in room_member_serializer.data:
            room_ids.add(room_member['room_id'])

        rooms = Room.objects.filter(id__in=room_ids)

        room_serializer = RoomSerializer(rooms, many=True)

        return Response(room_serializer.data, status=status.HTTP_200_OK)


    # def destroy(self, request, *args, **kwargs):
    #     print(kwargs.get('pk'))
    #
    #     room_id = kwargs.get('pk')
    #
    #     """
    #         STEP 1: Get rooms
    #         STEP 2: Get Channel
    #         STEP 3: Get Channel Members and Delete
    #         STEP 4: Delete Channels
    #         STEP 5: Delete Room
    #     """
    #
    #     try:
    #         with transaction.atomic():
    #             room = self.get_queryset().get(id=room_id)
    #
    #
    #     except Room.DoesNotExist:
    #         raise ValidationError({"error": f"Room with id {room_id} does not exist"})
    #
    #     return None

