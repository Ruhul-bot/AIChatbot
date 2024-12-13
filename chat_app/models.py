from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    intent = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']