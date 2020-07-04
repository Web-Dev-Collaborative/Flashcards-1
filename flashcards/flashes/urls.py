from django.urls import path

from flashcards.flashes import views

app_name = 'flashes'

urlpatterns = [
    path('', views.FlashcardListView.as_view(), name='list'),
    path('create/', views.FlashcardCreateView.as_view(), name='create'),
    path('<int:pk>', views.FlashcardDetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.FlashcardUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.FlashcardDeleteView.as_view(), name='delete')
]
