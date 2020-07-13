from django.urls import path

from . import views

app_name = 'leitner'

urlpatterns = [
    path('', views.DeckListView.as_view(), name='deck-list'),
    path('create/', views.DeckCreationView.as_view(), name='deck-create'),
    path('<int:deck_pk>/', views.DeckDetailView.as_view(), name='deck-detail'),  # Includes a box list
    path('<int:deck_pk>/add_box', views.BoxCreationView.as_view(), name='add-box'),
    path('<int:deck_pk>/<int:box_pk>', views.BoxDetailView.as_view(), name='view-box'),
    path('<int:deck_pk>/add_card', views.CardCreationView.as_view(), name='add-card'),
]
