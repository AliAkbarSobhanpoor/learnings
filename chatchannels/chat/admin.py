from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass