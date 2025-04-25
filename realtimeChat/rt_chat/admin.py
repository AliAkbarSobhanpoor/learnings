from django.contrib import admin
from . import models


@admin.register(models.ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RoomMessage)
class RoomMessageAdmin(admin.ModelAdmin):
    pass
