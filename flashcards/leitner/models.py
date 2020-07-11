from django.conf import settings
from django.db import models
from django.db.models import QuerySet

"""
Models for the Leitner System, see  https://en.wikipedia.org/wiki/Leitner_system
"""


class Deck(models.Model):
    description = models.CharField('Deck description', max_length=150)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='decks')

    def add_box(self, description: str) -> 'Box':
        """
        Adds a box to the current deck.

        Args:
            description (str): Description of the box

        Returns:
            Box: box created
        """
        new_box = Box.objects.create(description=description, deck=self)
        return new_box

    def get_boxes(self, ascending: bool = True) -> QuerySet:
        """
        Returns a queryset with the cards in the current box

        Args:
            ascending (bool): Order of the boxes in the queryset, if true (default) will be in ascending order
                              (cards added first will be before the newly added ones). If false boxes
                              will be in descending order (last added cards first).
        """
        if ascending:
            field = 'created_at'
        else:
            field = '-created_at'
        return self.boxes.order_by(field)


class Box(models.Model):
    description = models.CharField('Box description', max_length=150)
    deck = models.ForeignKey(to=Deck, on_delete=models.CASCADE, related_name='boxes')
    created_at = models.DateTimeField('Box creation date (determines box order)', auto_now_add=True)

    def get_cards(self, ascending: bool = True) -> QuerySet:
        """
        Returns a queryset with the cards in the current box

        Args:
            ascending (bool): Order of the card in the queryset, if true (default) will be in ascending order
                              (cards added first will be before the newly added ones). If false cards
                              will be in descending order (last added cards first).
        """
        if ascending:
            field = 'updated_at'
        else:
            field = '-updated_at'
        return self.cards.order_by(field)


class Card(models.Model):
    front_text = models.CharField('Front text', max_length=150)
    back_text = models.TextField('Back text')
    # color = ???? may use django-colorfield https://pypi.org/project/django-colorfield/
    updated_at = models.DateTimeField('Last modified on', auto_now=True)
    on_deck = models.ForeignKey(to=Deck, on_delete=models.SET_NULL, related_name='cards', null=True, default=None)
    on_box = models.ForeignKey(to=Box, on_delete=models.SET_NULL, related_name='cards', null=True, default=None)

    def move_to_box(self, box: Box) -> None:
        """
        Moves the card to the designated box

        Args:
            box (Box): Target box. Must be in the current deck, otherwise, KeyError will be raised.
        """
        if box not in self.on_deck.boxes.all():
            raise KeyError('Box not in the current deck')
        self.on_box = box
        self.save()
