from django.db import models

from api.Model.Comment import Comment
from api.Model.CustomUser import CustomUser


class SubmissionComment(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
