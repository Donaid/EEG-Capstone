# -*- coding: utf-8 -*-

from django.urls import path
from .consumers import WebsocketConnection
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

#create routing to channel
websocket_urlPattern = [
    path('ws/test1', WebsocketConnection.as_asgi()),
]

application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter(websocket_urlPattern))
})