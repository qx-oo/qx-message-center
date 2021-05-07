"""
ASGI config for qx_test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import qx_ws
from .auth import AioAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qx_test.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AioAuthMiddleware(
        URLRouter(
            qx_ws.routing.websocket_urlpatterns,
        )
    ),
})
