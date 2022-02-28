from django.shortcuts import render
from django.conf import settings

# Create your views here.

DEBUG = True


def home_screen_view(request):
    context = {
        'debug_mode': settings.DEBUG, 'debug': DEBUG, 'room_id': "1"
    }
    return render(request, "home.html", context)
