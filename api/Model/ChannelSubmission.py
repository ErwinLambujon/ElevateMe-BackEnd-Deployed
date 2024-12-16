import os
from uuid import uuid4

from django.core.validators import FileExtensionValidator
from django.db import models
def unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    original_name = os.path.splitext(filename)[0]
    unique_name = f"{original_name}_{uuid4()}.{ext}"
    return os.path.join('submissions', unique_name)

class ChannelSubmission(models.Model):
    submitted_work = models.FileField(
        upload_to=unique_filename,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf']
            )
        ],
    )
    problem_statement = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    member_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    channel_id = models.ForeignKey('RoomChannel', on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return f'Submission by {self.member_id.first_name} in {self.channel_id.channel_name} on {self.date_submitted}'