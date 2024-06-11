# chat/views.py
from django.shortcuts import render
from django.urls import reverse


def websocket_debug_index(request):
    return render(request, "websocket/debug/index.html")


def websocket_debug_chat_room(request, room_name):
    ws_method = "wss" if request.META.get(
        'HTTP_X_FORWARDED_PROTO', '') == 'https' else "ws"
    return render(request, "websocket/debug/room.html", {"room_name": room_name, "ws_method": ws_method, "websocket_debug_index_url": reverse('websocket_debug_index')})
