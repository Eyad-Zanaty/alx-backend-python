from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ThreadedMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threaded_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Key: Parent message (self-referential FK)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.sender.username} @ {self.timestamp:%Y-%m-%d %H:%M}'
