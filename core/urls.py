"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views

from account.views import register_view, login_view, logout_view, account_search_view

urlpatterns = [
    path('', include('chat.urls', namespace='private_chat')),
    path('account/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('friend/', include('friend.urls', namespace='friend')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('public', include('public_chat.urls', namespace='public_chat')),
    path('register/', register_view, name='register'),
    path('search/', account_search_view, name='search'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_link.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
