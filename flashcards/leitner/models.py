from typing import List

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

"""
Models for the Leitner System, see  https://en.wikipedia.org/wiki/Leitner_system
"""


class Card(models.Model):
    front_text = models.CharField('Front text', max_length=150)
    back_text = models.TextField('Back text')
    # color = ???? may use django-colorful https://pypi.org/project/django-colorful/
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cards')
    updated_at = models.DateTimeField('Last modified on', auto_now=True)
    # The idea is to make every card independent from the box it is contained,
    # this way, if you delete a box you don't lose every card on it
    boxes = models.ManyToManyField(to='Box', through='CardBoxRelation')


class Box(models.Model):
    description = models.CharField('Box description', max_length=150)
    session = models.ForeignKey(to='Session', on_delete=models.CASCADE)
    position = models.IntegerField('Position of the box in the session')

    def cards_in_box(self) -> QuerySet:
        """
        Returns: A queryset including every Card object in the current box
        """
        # Note to myself: This is possible because of the ManyToManyField
        return self.card_set.all()

    def add_card(self, card: Card, where='last'):
        """
        Adds a card to the current box

        Args:
            card: Card object to add, if card is already in the session or box KeyError will be raised
            where: What position to add the card, 'first' will add it to the first position, moving
                   other cards one position up (similar to deque.appendleft), 'last' will add it to the
                   last position (similar to list.append). Any other value will raise ValueError
        """
        if card in self.session.list_cards_in_session():
            raise AttributeError('Card already in the session')  # ToDo: Find a better exception to use
        if where not in ('first', 'last'):
            raise ValueError('Can only assign on first or last position')
        if where == 'last':
            card_position = len(self.cards_in_box())
        elif where == 'first':
            card_position = 0
            for relation in self.cardboxrelation_set.all():
                relation.card_position_in_box += 1
                relation.save()

        CardBoxRelation.objects.create(
            card=card,
            box=self,
            card_position_in_box=card_position
        )

    def delete_card(self, card: Card) -> None:
        """
        Deletes a card from the current box. The cards get reordered after the deletion

        Args:
            card: card to delete
        """
        if card not in self.cards_in_box():
            raise KeyError('Card not in the current box')
        card.cardboxrelation_set.filter(box=self).delete()
        self._reorder_cards()

    def move_card_to_box(self, card: Card, other_box: 'Box', where: str = 'last') -> None:
        """
        Moves a card from the current box to another box. Internally it calls the
        box.delete_card, box_reorder_cards and other_box.add_card methods.

        Args:
            card: Card to move to another box. Must be included in the current box.
            other_box: Where to move the card
            where: 'first' appends left, 'last' appends right. Any other value raises ValueError.
                    See Box.add_card docstring for more details
        """
        self.delete_card(card)
        self._reorder_cards()
        other_box.add_card(card, where=where)

    def _reorder_cards(self) -> None:
        """
        Reorders every card position number in the box when a card is moved or deleted
        """
        for idx, relation in enumerate(self.cardboxrelation_set.all().order_by('card_position_in_box')):
            if relation.card_position_in_box != idx:
                relation.card_position_in_box = idx
                relation.save()


class Session(models.Model):
    description = models.CharField('Session description', max_length=150)
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    stage = models.IntegerField(default=0)  # Times the session has been ran
    is_running = models.BooleanField(default=False)

    def add_box(self, description: str) -> Box:
        """
        Creates and adds a box to the current session, it is added in the last position

        Args:
            description: Box description

        Returns:
            Box: box created
        """
        box = Box.objects.create(description=description,
                                 session=self,
                                 position=len(self.box_set.all()))
        return box

    def delete_box(self, box: Box) -> None:
        """
        Deletes a box from the current session and reorders the remaining boxes.

        Args:
            box: Box to delete
        """
        if box not in self.box_set.all():
            raise AttributeError('Box is not in the current session')  # ToDo: Find a better exception to use
        box.delete()
        self._reorder_boxes()

    def _reorder_boxes(self) -> None:
        """
        Reorders every box position, starting from 0
        """
        boxes_queryset = self.box_set.all().order_by('position')
        for idx, box in enumerate(boxes_queryset):
            if box.position != idx:
                box.position = idx
                box.save()

    def list_cards_in_session(self) -> List[Card]:
        """
        Returns: A list of card objects that are in the current session
        """
        # FixMe: I should get a queryset instead of creating a list
        cards = []
        for box in self.box_set.all():
            for card_box_relation in box.cardboxrelation_set.all():
                cards.append(card_box_relation.card)
        return cards


class CardBoxRelation(models.Model):
    """ Junction table """
    card = models.ForeignKey(Card, models.CASCADE, null=False)
    box = models.ForeignKey(Box, models.CASCADE, null=False)
    card_position_in_box = models.IntegerField('Position number of the card in the box')
