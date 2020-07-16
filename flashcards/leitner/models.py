from typing import Union

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

"""
Models for the Leitner System, see  https://en.wikipedia.org/wiki/Leitner_system
"""


class Deck(models.Model):
    description = models.CharField('Deck description', max_length=150)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='decks')

    def create_boxes(self):
        defaults = {'in_session': False, 'last_used': None, 'deck': self}
        Box.objects.create(description='Use this every day', box_type=0, **defaults)
        Box.objects.create(description='Use this every tuesday and thursday', box_type=1, **defaults)
        Box.objects.create(description='Use this every friday', box_type=2, **defaults)

    def __str__(self):
        return self.description


class Box(models.Model):
    description = models.CharField('Box description', max_length=150)
    deck = models.ForeignKey(to=Deck, on_delete=models.CASCADE, related_name='boxes')
    in_session = models.BooleanField('Box currently in session?', default=False)
    box_type = models.IntegerField('0: Everyday, 1: Tue/Thu, 2: Fri')
    last_used = models.DateTimeField(null=True)

    def get_cards(self, ascending: bool = False) -> QuerySet:
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

    def last_used_text(self):
        return 'Never' if self.last_used is None else self.last_used.strftime('%a %d %b %Y %H:%M')

    def __str__(self):
        return f'Box: {self.description} | Last used: {self.last_used_text()}'


class Card(models.Model):
    front_text = models.CharField('Front text', max_length=150)
    back_text = models.TextField('Back text')
    updated_at = models.DateTimeField('Last modified on', auto_now=True)
    on_deck = models.ForeignKey(to=Deck, on_delete=models.CASCADE, related_name='cards')
    on_box = models.ForeignKey(to=Box, on_delete=models.CASCADE, related_name='cards')

    def correct_answer(self) -> None:
        """
        Moves the card to the next box, given a correct answer
        """
        if self.on_box.box_type == 0:
            self.on_box = self.on_deck.boxes.get(box_type=1)
            self.save()
        elif self.on_box.box_type == 1:
            self.on_box = self.on_deck.boxes.get(box_type=2)
            self.save()
        SessionFinishedCards.objects.create(session=self.on_deck.session.get(), card=self)
        # Nothing happens if it is on box type 3

    def wrong_answer(self) -> None:
        """
        Moves the card to the box type 0, given a wrong answer
        """
        self.on_box = self.on_deck.boxes.get(box_type=0)
        self.save()
        SessionFinishedCards.objects.create(session=self.on_deck.session.get(), card=self)


class Session(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='session')
    current_box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='session')
    total_cards_on_box = models.IntegerField('Total cards of the current box')
    is_finished = models.BooleanField('Is the session finished?', default=False)

    def current_card(self) -> Union[Card, None]:
        finished_cards = Card.objects.filter(finished_session__session=self)
        for card in self.current_box.get_cards():
            if card not in finished_cards:
                return card
        return None


class SessionFinishedCards(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='finished_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='finished_session')
