from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'chat/index.html')


def room(request: HttpRequest, room_name) -> HttpResponse:
    return render(request, 'chat/room.html', {"room_name": room_name})

