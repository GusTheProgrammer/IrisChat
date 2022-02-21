from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'birth_date', 'email', 'bio')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        class Meta:
            model = CustomUser
            fields = ('first_name', 'last_name', 'birth_date', 'email', 'bio')