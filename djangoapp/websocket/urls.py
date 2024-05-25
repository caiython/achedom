# chat/urls.py
from django.urls import path
from django.conf import settings

from . import views


urlpatterns = [

]

if settings.DEBUG:
    urlpatterns += [
        path("debug/", views.websocket_debug_index,
             name="websocket_debug_index"),
        path("debug/<str:room_name>/", views.websocket_debug_chat_room,
             name="websocket_debug_chat_room"),
    ]
