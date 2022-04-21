from django.urls import path

from .views import home_screen_view, create_public_chat

app_name = 'chat'

urlpatterns = [
    path('', home_screen_view, name='public_chat_view'),
    path('create_public_chat/', create_public_chat, name='create_public_chat'),
]
