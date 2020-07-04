from django.contrib import admin

from flashcards.users.models import User
from flashcards.flashes.models import Flash

admin.site.register(User)
admin.site.register(Flash)
