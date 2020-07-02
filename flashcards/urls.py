from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('account/', include('flashcards.users.urls', namespace='users')),
    path('flashcards/', include('flashcards.flashes.urls', namespace='flashes'))
]