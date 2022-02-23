from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, StartPageView

urlpatterns = [
    path('', StartPageView.as_view(), name='homepage'),
    path('login/',
         auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

]
