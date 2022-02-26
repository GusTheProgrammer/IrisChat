from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

from .forms import RegistrationForm, AccountAuthenticationForm
from .models import Account


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)  # might occur issues
            if destination:  # if destination != None
                return redirect(destination)
            return redirect('homepage')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("homepage")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("homepage")

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
                return redirect("homepage")

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
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        # context['BASE_URL'] = settings.BASE_URL
        return render(request, "account/account.html", context)


def account_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(
                username__icontains=search_query).distinct()
            user = request.user
            accounts = []  # [(account1, True), (account2, False), ...]
            for account in search_results:
                accounts.append((account, False))  # you have no friends yet
            context['accounts'] = accounts

    return render(request, "account/search_results.html", context)
