from django.urls import path
from . import views


"""
    we have 4 views. each for each tipe of communications.
    rooms has 3 type for now :
        1. rooms are public.
        2. channels are public. only owners can send message.
        3. groups are private . everyone can send data.
        4. private this pryvate.
"""
urlpatterns = [
    path("room/<str:room_name>/", views.chat_room_view, name="chat_index"),
]