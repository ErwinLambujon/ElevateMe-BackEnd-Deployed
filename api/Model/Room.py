import uuid

from django.db import models

from api.Model.CustomUser import CustomUser


class Room(models.Model):
    room_name = models.TextField()
    room_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    room_owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room_name}'