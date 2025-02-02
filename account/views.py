import base64
import json
import os
import cv2

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.core import files
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from .models import Account

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


# This is basically almost exactly the same as friends/friend_list_view
def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(
                username__icontains=search_query).distinct()
            user = request.user
            accounts = []  # [(account1, True), (account2, False), ...]
            if user.is_authenticated:
                # get the authenticated users friend list
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts

    return render(request, "account/search_results.html", context)


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        # return HttpResponse("You are already authenticated as " + str(user.email))
        return redirect('public_chat:public_chat_view')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('public_chat:public_chat_view')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("public_chat:public_chat_view")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("public_chat:public_chat_view")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("public_chat:public_chat_view")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def account_view(request, *args, **kwargs):
    """
    - Logic here is kind of tricky
        is_self (boolean)
            is_friend (boolean)
                -1: NO_REQUEST_SENT
                0: THEM_SENT_TO_YOU
                1: YOU_SENT_TO_THEM
    """
    global can_view
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['bio'] = account.bio
        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['birth_date'] = account.birth_date
        context['profile_image'] = account.profile_image.url
        context['hide_info'] = account.hide_info
        context['hide_friends'] = account.hide_friends

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends

        # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value  # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass

        # Friend List
        user = request.user
        if user.is_authenticated:
            if user_id:
                try:
                    this_user = Account.objects.get(pk=user_id)
                    context['this_user'] = this_user
                except Account.DoesNotExist:
                    return HttpResponse("That user does not exist.")
                try:
                    friend_list = FriendList.objects.get(user=this_user)
                except FriendList.DoesNotExist:
                    return HttpResponse(f"Could not find a friends list for {this_user.username}")

                # Must be friends to view a friends list
                can_view = True

                if user != this_user:
                    if not user in friend_list.friends.all():
                        can_view = False
                friends = []  # [(friend1, True), (friend2, False), ...]
                # get the authenticated users friend list
                auth_user_friend_list = FriendList.objects.get(user=user)
                for friend in friend_list.friends.all():
                    friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
                context['friends'] = friends

        # Set the template variables to the values
        context['can_view'] = can_view
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_DIR
        return render(request, "account/account.html", context)


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(f"{settings.TEMP}/{user.pk}"):
            os.mkdir(f"{settings.TEMP}/{user.pk}")
        url = os.path.join(f"{settings.TEMP}/{user.pk}", TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print("exception: " + str(e))
        # workaround for an issue I found
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
    return None


def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))
            cropRotate = int(float(str(request.POST.get("cropRotate"))))
            if cropX < 0:
                cropX = 0
            if cropY < 0:  # There is a bug with cropperjs. y can be negative.
                cropY = 0

            if cropRotate == 90:
                final_img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
            elif cropRotate == 180:
                final_img = cv2.rotate(img, cv2.cv2.ROTATE_180)
            elif cropRotate == 270:
                final_img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                final_img = img

            crop_img = final_img[cropY:cropY + cropHeight, cropX:cropX + cropWidth]
            cv2.imwrite(url, crop_img)

            # delete the old image
            user.profile_image.delete()

            # Save the cropped image to user model
            user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
            user.save()

            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url

            # delete temp file
            os.remove(url)

        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    return HttpResponse(json.dumps(payload), content_type="application/json")


def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account:view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                                     initial={"id": account.pk, "email": account.email, "username": account.username,
                                              "profile_image": account.profile_image, "first_name": account.first_name,
                                              "last_name": account.last_name, "bio": account.bio,
                                              "birth_date": account.birth_date, "hide_info": account.hide_info,
                                              "hide_friends": account.hide_friends, })
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                "id": account.pk,
                "email": account.email,
                "username": account.username,
                "profile_image": account.profile_image,
                "first_name": account.first_name,
                "last_name": account.last_name,
                "bio": account.bio,
                "birth_date": account.birth_date,
                "hide_info": account.hide_info,
                "hide_friends": account.hide_friends,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_account.html", context)
