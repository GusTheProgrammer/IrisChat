import json
import pytz

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .models import PublicChatRoom, PublicRoomChatMessage

# Create your views here.

DEBUG = False


def home_screen_view(request):
    user = request.user

    rooms = PublicChatRoom.objects.all()
    groups = []
    for room in rooms:
        try:
            message = PublicRoomChatMessage.objects.filter(room=room).latest("timestamp")
        except PublicRoomChatMessage.DoesNotExist:
            # create a dummy message with dummy timestamp
            today = datetime(
                year=1950,
                month=1,
                day=1,
                hour=1,
                minute=1,
                second=1,
                tzinfo=pytz.UTC
            )
            message = PublicRoomChatMessage(
                room=room,
                timestamp=today,
                content="",
            )
        groups.append({
            "room": room,
            "message": message,
        })
        room_id = room.id

    room = PublicChatRoom.objects.get(pk=room_id)
    room_title = room.title

    context = {}
    context['groups'] = groups
    context['debug'] = DEBUG
    context['debug_mode'] = settings.DEBUG

    if user.is_authenticated:
        return render(request, "public_chat/public_chat_room.html", context)
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
