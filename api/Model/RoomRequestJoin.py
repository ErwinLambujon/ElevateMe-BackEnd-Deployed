from django.db import models

class RoomRequestJoin(models.Model):
    """
        Payload: {
            user_id - Whos joining the room
            room_id - What room is he joining
            request_timestamp - What date did he requested to join
        }
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed')
    ]

    date_requested = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-date_requested']

    @classmethod
    def can_create_request(cls, user, room):
        return not cls.objects.filter(user=user, room=room, status__in=['pending', 'approved']).exists()