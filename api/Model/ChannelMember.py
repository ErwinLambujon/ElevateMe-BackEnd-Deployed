from django.db import models

from api.Model.CustomUser import CustomUser
from api.Model.RoomChannel import RoomChannel


class ChannelMember(models.Model):
    joined_date = models.DateTimeField(auto_now_add=True)
    member_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Reference on member
    channel_id = models.ForeignKey(RoomChannel, on_delete=models.CASCADE)  # Reference on what channel

    def __str__(self):
        return f'{self.member_id.email} joined on {self.joined_date}'
