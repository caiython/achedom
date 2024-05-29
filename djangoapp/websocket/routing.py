from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/debug/(?P<room_name>\w+)/$",
            consumers.DebugChatConsumer.as_asgi()),
    re_path(r"ws/update_component/$",
            consumers.ComponentConsumer.as_asgi(), name='ws_update_component'),
]
