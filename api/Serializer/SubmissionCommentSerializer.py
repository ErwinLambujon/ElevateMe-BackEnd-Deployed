from rest_framework import serializers

from api.Model.SubmissionComment import SubmissionComment


class SubmissionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionComment
        fields = '__all__'