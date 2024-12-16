from rest_framework import serializers

from api.Model.SubmissionVoting import SubmissionVotingMark


class SubmissionVotingMarkSerializer(serializers.ModelSerializer):
    voter_type = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionVotingMark
        fields = '__all__'

    def get_voter_type(self, obj):
        # Since member_id is actually a ForeignKey to CustomUser,
        # we can access the user_type directly
        return obj.member_id.user_type  # Using member_id since that's your field name