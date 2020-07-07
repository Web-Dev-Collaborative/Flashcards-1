from django.urls import path

from flashcards.notes import views

app_name = 'notes'

urlpatterns = [
    path('', views.NoteListView.as_view(), name='list'),
    path('create/', views.NoteCreateView.as_view(), name='create'),
    path('<int:pk>', views.NoteDetailView.as_view(), name='detail'),
    path('<int:pk>/update', views.NoteUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.NoteDeleteView.as_view(), name='delete')
]
