from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from .models import ChatRoom, RoomMessage
from .forms import ChatMessageCreateForm


@login_required
def chat_room_view(request: HttpRequest, room_name: str) -> HttpResponse:
    room = ChatRoom.objects.get_or_create(room_name=room_name)[0] # return obj, created : the second one no matter.
    # todo: implement a welcome message for the rooms from admin. that work dynamically.
    room_messages = RoomMessage.objects.filter(room__room_name=room.room_name)[:30]
    form: ChatMessageCreateForm = ChatMessageCreateForm()
    if request.htmx:
        form : ChatMessageCreateForm = ChatMessageCreateForm(request.POST)
        if form.is_valid:
            message:RoomMessage = form.save(commit=False)
            message.author = request.user
            message.room = room
            message.save()
            return render(request, "rt_chat/partials/chat_message.html", context={
                "message": message,
                "user": request.user
            })
    return render(request, 'rt_chat/chat.html', {
        "room_messages": room_messages, "form": form, "room": room
    })
