from django.urls import path

from . import views

app_name = 'leitner'

urlpatterns = [
    path('', views.DeckListView.as_view(), name='deck-list'),
    path('<int:pk>/', views.DeckDetailView.as_view(), name='deck-detail'),  # Includes a box list
    path('<int:deck_pk>/session', views.StudySession.as_view(), name='session'),
    path('<int:deck_pk>/add_box', views.BoxCreationView.as_view(), name='add-box'),
    path('<int:deck_pk>/<int:box_pk>', views.BoxDetailView.as_view(), name='view-box'),
    path('<int:deck_pk>/add_card', views.CardCreationView.as_view(), name='add-card'),
    path('<int:deck_pk>/cards', views.CardListView.as_view(), name='card-list'),
    path('<int:deck_pk>/cards/<int:card_pk>', views.CardUpdateView.as_view(), name='card-update'),
    path('<int:deck_pk>/cards/<int:card_pk>/delete', views.CardDeleteView.as_view(), name='card-delete'),
]
