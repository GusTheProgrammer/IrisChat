import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .models import PublicChatRoom

# Create your views here.

DEBUG = False


def home_screen_view(request):
    user = request.user

    rooms = PublicChatRoom.objects.all()
    groups = []
    for room in rooms:
        groups.append({
            "room": room,
        })
        room_id = room.id

    room = PublicChatRoom.objects.get(pk=room_id)
    room_title = room.title

    context = {}
    context['groups'] = groups
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG

    if user.is_authenticated:
        return render(request, "home.html", context)
    else:
        return redirect('login')


def create_public_chat(request, *args, **kwargs):
    user = request.user
    payload = {}
    if user.is_authenticated:
        if request.method == "POST":
            room_id = request.POST.get("public_room_id")
            print(room_id)
            try:
                try:
                    chat = PublicChatRoom.objects.get(id=room_id)
                except PublicChatRoom.DoesNotExist:
                    try:
                        chat = PublicChatRoom.objects.get(id=room_id)
                    except PublicChatRoom.DoesNotExist:
                        chat = PublicChatRoom(id=room_id)
                        chat.save()
                payload['response'] = "Successfully got the chat."
                payload['chatroom_id'] = chat.id
            except PublicChatRoom.DoesNotExist:
                payload['response'] = "Unable to start a chat with that user."
    else:
        payload['response'] = "You can't start a chat if you are not authenticated."
    return HttpResponse(json.dumps(payload), content_type="application/json")




