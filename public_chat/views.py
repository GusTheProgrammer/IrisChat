from django.shortcuts import render, redirect
from django.conf import settings

from .models import PublicChatRoom

# Create your views here.

DEBUG = False


def home_screen_view(request):
    user = request.user

    group_id = request.GET.get("room_id")
    print("########################################################", group_id)

    rooms = PublicChatRoom.objects.all()
    groups = []
    for room in rooms:
        groups.append({
            "id": room.id,
            "title": room.title,
            "users": room.users
        })

    room_id = 1
    room = PublicChatRoom.objects.get(pk=room_id)
    room_title = room.title

    context = {}
    context['groups'] = groups
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG
    context['room_id'] = room_id
    context['room_title'] = room_title

    if user.is_authenticated:
        return render(request, "home.html", context)
    else:
        return redirect('login')
