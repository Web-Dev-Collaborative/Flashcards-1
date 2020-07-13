from django.contrib import admin

from flashcards.leitner.models import Deck, Card, Box
from flashcards.users.models import User
from flashcards.notes.models import Note

admin.site.register(User)
admin.site.register(Note)
admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(Box)
