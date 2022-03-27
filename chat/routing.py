from django.urls import path

from public_chat.consumers import PublicChatConsumer
from chat.consumers import ChatConsumer
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path("", NotificationConsumer.as_asgi()),
    path("chat/<room_id>/", ChatConsumer.as_asgi()),
    path("public_chat/<room_id>/", PublicChatConsumer.as_asgi())

]
