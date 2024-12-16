from django.db import models

from api.Model.CustomUser import CustomUser
from api.Model.Room import Room


class RoomMember(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.member_id.email} joined on {self.joined_date}'