from email.mime import application
import imp
from django.http import HttpResponse
import json

from account.models import Account
from friends.models import FriendRequest

def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender = user, receiver = receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a frind request.")
                    friend_request = FriendRequest(sender = user , receiver = receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender = user, receiver = receiver)
                friend_request.save()
                payload["response"] = "Friend request sent."

            if payload["response"] == None:
                payload["response"] = "Something went wrong."       
        else:
            payload["response"] = "Unable to send a frind request."
    else:
        payload["response"] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type = "application/json")