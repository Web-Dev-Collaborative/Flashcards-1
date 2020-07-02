from django.db import models
from django.urls import reverse
from datetime import datetime
from django.conf import settings


class Flash(models.Model):
    """ Flashcard model """
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content')
    last_change_date = models.DateTimeField('Last modified on', default=datetime.now)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flashes:detail', kwargs={"username": self.created_by, "pk": self.pk})
