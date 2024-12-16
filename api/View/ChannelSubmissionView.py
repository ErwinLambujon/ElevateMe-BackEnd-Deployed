import boto3
from django.conf import settings
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.RoomChannel import RoomChannel
from api.Serializer.ChannelSubmissionSerializer import ChannelSubmissionSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import logging


class ChannelSubmissionView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ChannelSubmissionSerializer
    queryset = ChannelSubmission.objects.all
    parser_classes = (MultiPartParser, FormParser)  # Add this line if not already present
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChannelSubmission.objects.filter(channel_id=self.kwargs['channel_pk'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        print(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def submit(self, request, channel_pk=None):
        try:
            channel = RoomChannel.objects.get(id=channel_pk)
        except RoomChannel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)

        file_obj = request.FILES.get('submitted_work')
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        submission_data = {'channel_id': channel.id, 'member_id': request.user.id,
                           'problem_statement': request.data.get('problem_statement', ''), 'submitted_work': file_obj}

        try:
            serializer = self.get_serializer(data=submission_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Serializer errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'], url_path='download')
    def download_submission(self, request, pk=None, channel_pk=None):
        submission = get_object_or_404(ChannelSubmission, id=pk, channel_id=channel_pk)
        logger = logging.getLogger(__name__)

        if not submission.submitted_work:
            raise Http404("File not found")

        try:
            logger.info(f"Attempting to download file: {submission.submitted_work.name}")
            return FileResponse(
                submission.submitted_work.open('rb'),
                as_attachment=True,
                filename=submission.submitted_work.name
            )
        except FileNotFoundError:
            logger.error("File not found error")
            raise Http404("File not found")
