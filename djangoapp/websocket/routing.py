from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/debug/(?P<room_name>\w+)/$",
            consumers.DebugChatConsumer.as_asgi()),
]
