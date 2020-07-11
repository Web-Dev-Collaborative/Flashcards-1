import pytest
from django.test import TestCase

from flashcards.leitner.models import Card, Deck
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestLeitnerModels(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='TestUser', password='testing321')
        self.deck = Deck.objects.create(description='Learning german', created_by=self.user)
        self.card_list = [
            Card.objects.create(front_text=f'Card front {i}', back_text=f'Card back {i}',
                                on_deck=self.deck)
            for i in range(10)
        ]

    def test_adding_boxes_to_deck(self):
        box0 = self.deck.add_box(description='Use this every day')
        box1 = self.deck.add_box(description='Use this every other day')
        # Test there are two boxes on the deck
        self.assertEquals(self.deck.boxes.count(), 2)
        # Test on ascending order
        box_qs = self.deck.get_boxes(ascending=True)
        self.assertEquals(box_qs[0], box0)
        self.assertEquals(box_qs[1], box1)
        # Test on descending order
        box_qs = self.deck.get_boxes(ascending=False)
        self.assertEquals(box_qs[0], box1)
        self.assertEquals(box_qs[1], box0)

    def test_get_cards_from_box(self):
        box0 = self.deck.add_box(description='Use this every day')
        box1 = self.deck.add_box(description='Use this every other day')

        boxes = [box0, box1]

        for i, card in enumerate(self.card_list):
            card.move_to_box(boxes[i % 2])

        self.assertEquals(box0.cards.count(), 5)
        self.assertEquals(box1.cards.count(), 5)

    def test_adding_card_from_other_deck(self):
        new_deck = Deck.objects.create(
            description='English course',
            created_by=self.user
        )
        new_box = new_deck.add_box(description='use this every day')

        self.assertRaises(KeyError, self.card_list[0].move_to_box, new_box)

    def test_cards_order_in_box(self):
        box0 = self.deck.add_box('Box 0')

        for i in range(5):
            self.card_list[i].move_to_box(box0)

        for i, card in enumerate(box0.get_cards(ascending=True)):
            self.assertEquals(card, self.card_list[i])

        for i, card in enumerate(box0.get_cards(ascending=False)):
            self.assertEquals(card, self.card_list[4 - i])
