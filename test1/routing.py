# -*- coding: utf-8 -*-

from django.urls import path
from .consumers import GraphConsumer
from .consumers import test2
#create routing to channel
ws_urlpatterns = [
    path('ws/mysitedddd/', test2.as_asgi())
]
