from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'first_name', 'last_name', 'birth_date', 'profile_pic']
    list_editable = ['profile_pic']


admin.site.register(CustomUser, CustomUserAdmin)
