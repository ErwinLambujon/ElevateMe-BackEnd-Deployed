from django.db import transaction
from rest_framework import serializers

from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.Comment import Comment
from api.Model.SubmissionComment import SubmissionComment


class CommentSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()
    content = serializers.CharField()
    commented_on = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

    def get_author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def create(self, validated_data):
        submission = validated_data.get('submission_id')
        member = self.context['request'].user

        if not isinstance(submission, ChannelSubmission):
            raise serializers.ValidationError({"error": "Invalid submission provided"})

        with transaction.atomic():
            comment = Comment.objects.create(**validated_data)
            SubmissionComment.objects.create(comment_id=comment, member_id=member)

        return comment
