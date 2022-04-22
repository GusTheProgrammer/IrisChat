from django.urls import path

from chat.consumers import ChatConsumer
from notification.consumers import NotificationConsumer
from public_chat.consumers import PublicChatConsumer

websocket_urlpatterns = [
    path("", NotificationConsumer.as_asgi()),
    path("chat/<room_id>/", ChatConsumer.as_asgi()),
    path("public_chat/<room_id>/", PublicChatConsumer.as_asgi())

]
