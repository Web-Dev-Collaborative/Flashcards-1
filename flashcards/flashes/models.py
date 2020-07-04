from django.conf import settings
from django.db import models
from django.urls import reverse


class Flash(models.Model):
    """ Flashcard model """
    title = models.CharField('Title', max_length=200)
    content = models.TextField('Content')
    updated_at = models.DateTimeField('Last modified on', auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flashes:detail', args=(self.pk,))
