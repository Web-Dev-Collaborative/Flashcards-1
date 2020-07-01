from django.urls import path

from flashcards.flashes import views

app_name = 'flashes'

urlpatterns = [
    path('', views.FlashcardListView.as_view(), name='list'),
    path('create/', views.FlashcardCreateView.as_view(), name='create'),
]
