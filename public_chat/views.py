from django.shortcuts import render, redirect
from django.conf import settings

from .models import PublicChatRoom

# Create your views here.

DEBUG = False


def home_screen_view(request):
    room_id = 2
    room = PublicChatRoom.objects.get(pk=room_id)
    room_title = room.title

    context = {
        'debug_mode': settings.DEBUG,
        'debug': DEBUG,
        'room_id': room_id,
        'room_title': room_title,
    }
    user = request.user
    if user.is_authenticated:
        return render(request, "home.html", context)
    else:
        return redirect('login')
