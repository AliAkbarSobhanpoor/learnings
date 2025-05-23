from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatMessage(models.Model):
    # because users can be anonymous here . and black user mean anonymous
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user if self.user else "anonymous"} @ room {self.room} - {self.timestamp}'
