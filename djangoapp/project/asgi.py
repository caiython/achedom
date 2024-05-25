"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from websocket.routing import websocket_urlpatterns
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django_asgi_app = get_asgi_application()
websocket = AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(
    websocket_urlpatterns))) if not settings.DEBUG else AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": websocket
    }
)
