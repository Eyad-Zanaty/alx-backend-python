from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:30]}"


class UnreadNotificationManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user, is_read=False).only('id', 'message', 'created_at')


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ edited Custom Manager
    objects = models.Manager()  # default
    unread = UnreadNotificationManager()  # custom

    def __str__(self):
        return f"Notification for {self.user.username} about message {self.message.id}"

