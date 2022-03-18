from django.shortcuts import render
from django.conf import settings

# Create your views here.

DEBUG = False


def home_screen_view(request):
    context = {
        'debug_mode': settings.DEBUG,
        'debug': DEBUG,
        'room_id': "1",
        'room_name': "General"
    }
    return render(request, "home.html", context)
