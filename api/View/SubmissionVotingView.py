from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.Model.SubmissionVoting import SubmissionVotingMark
from api.Serializer.SubmissionVotingSerializer import SubmissionVotingMarkSerializer


class SubmissionVotingMarkView(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionVotingMarkSerializer

    def get_queryset(self):
        submission_id = self.kwargs['submission_pk']
        # Use select_related with the actual field name
        return SubmissionVotingMark.objects.filter(submission_id=submission_id).select_related('member_id')

    def create(self, request, *args, **kwargs):
        submission_id = kwargs.get('submission_pk')
        marks = request.data.get('marks')

        if not marks or not isinstance(marks, (int, float)):
            return Response(
                {"error": "Invalid marks value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_vote = self.get_queryset().filter(member_id=request.user).first()

        if existing_vote:
            # Update existing vote
            existing_vote.marks = marks
            existing_vote.save()
            return Response(
                self.get_serializer(existing_vote).data,
                status=status.HTTP_200_OK
            )

        # Create new vote
        serializer = self.get_serializer(data={
            "marks": marks,
            "submission_id": submission_id,
            "member_id": request.user.id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )