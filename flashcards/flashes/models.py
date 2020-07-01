from django.db import models
from django.utils.datetime_safe import datetime
from django.conf import settings


class Flash(models.Model):
    """ Flashcard model """
    title = models.CharField('Flashcard title', max_length=200)
    content = models.TextField('Contents')
    last_change_date = models.DateTimeField('Creation date', default=datetime.now)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
