from django.urls import path
from . import views

app_name = 'users'  # TODO: What does this do?

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('', views.UserDetailsView.as_view(), name='user')
]
