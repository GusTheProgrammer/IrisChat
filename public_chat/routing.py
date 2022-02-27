from django.urls import path

from .consumers import PublicChatConsumer

websocket_urlpatterns = [
    path("public_chat/<room_id>/", PublicChatConsumer.as_asgi())
]
