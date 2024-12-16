from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.Model.Comment import Comment
from api.Model.SubmissionComment import SubmissionComment
from api.Serializer.CommentSerializer import CommentSerializer
from api.Serializer.SubmissionCommentSerializer import SubmissionCommentSerializer


class SubmissionCommentView(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        submission_id = self.kwargs['submission_pk']
        # Return comments associated with the given submission_id
        return Comment.objects.filter(submission_id=submission_id)

    def create(self, request, *args, **kwargs):
        submission_id = kwargs.get('submission_pk')
        content = request.data.get('content')
        author = request.user  # Get the logged-in user

        serializer = self.get_serializer(data={
            "content": content,
            "submission_id": submission_id,
            "author": author.id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Commented successfully"}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)  # Use CommentSerializer here
        return Response(serializer.data, status=status.HTTP_200_OK)

