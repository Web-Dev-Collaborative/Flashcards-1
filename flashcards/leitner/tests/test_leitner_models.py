import pytest
from django.test import TestCase

from flashcards.leitner.models import Deck, Box, Card
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestLeitnerModelsBasics(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.cl', 'testing321')

    def test_box_creation(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        deck.create_boxes()
        self.assertEquals(Box.objects.filter(deck=deck).count(), 3)

    def text_deck_str_method(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        self.assertEquals(str(deck), 'Test deck')
        self.assertEquals(deck.__str__(), 'Test deck')

    def text_box_str_method(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        box = Box.objects.create(description='Nothing interesting',
                                 deck=deck, box_type=0)
        self.assertEquals(str(box), 'Box: Nothing interesting | Last used: Never')


class TestLeitnerModelsMethods(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.cl', 'testing321')
        self.deck = Deck.objects.create(description='Test deck', created_by=self.user)
        self.deck.create_boxes()

    def test_box_cards_ascending(self):
        box = Box.objects.last()
        card1 = Card.objects.create(front_text='Card 1', back_text='Card 1',
                                    on_deck=self.deck, on_box=box)
        card2 = Card.objects.create(front_text='Card 2', back_text='Card 2',
                                    on_deck=self.deck, on_box=box)
        card3 = Card.objects.create(front_text='Card 3', back_text='Card 3',
                                    on_deck=self.deck, on_box=box)
        asc_qs = box.get_cards(ascending=True)
        self.assertEquals(asc_qs[0], card1)
        self.assertEquals(asc_qs[1], card2)
        self.assertEquals(asc_qs[2], card3)

    def test_card_methods(self):
        pass