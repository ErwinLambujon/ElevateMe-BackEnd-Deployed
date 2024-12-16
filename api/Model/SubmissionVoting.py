from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.Model.ChannelSubmission import ChannelSubmission
from api.Model.CustomUser import CustomUser


class SubmissionVotingMark(models.Model):
    marks = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Value must be at least 1"),
            MaxValueValidator(10, message="Value cannot be greater than 10")
        ]
    )
    submission_id = models.ForeignKey(ChannelSubmission, on_delete=models.CASCADE)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)