from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.UserDetailsView.as_view(),
         name='userdetails'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/login.html'),
         name='password_change')
]
