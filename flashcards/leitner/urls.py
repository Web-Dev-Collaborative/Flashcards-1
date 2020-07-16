from django.urls import path

from . import views

app_name = 'leitner'

urlpatterns = [
    path('', views.DeckListView.as_view(), name='deck-list'),
    path('<int:deck_pk>/', views.DeckDetailView.as_view(), name='deck-detail'),
    path('<int:pk>/delete', views.DeckDeleteView.as_view(), name='deck-delete'),
    path('<int:deck_pk>/session', views.SessionStartView.as_view(), name='session'),
    path('<int:deck_pk>/session/cards', views.SessionCardsView.as_view(), name='session-cards'),
    path('<int:deck_pk>/session/finished', views.SessionFinishedView.as_view(), name='session-finished'),
    path('<int:deck_pk>/add_card', views.CardCreationView.as_view(), name='add-card'),
    path('<int:deck_pk>/cards/<int:card_pk>', views.CardUpdateView.as_view(), name='card-update'),
    path('<int:deck_pk>/cards/<int:card_pk>/delete', views.CardDeleteView.as_view(), name='card-delete'),
]
