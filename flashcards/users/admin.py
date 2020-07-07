from django.contrib import admin

from flashcards.users.models import User
from flashcards.notes.models import Note

admin.site.register(User)
admin.site.register(Note)
