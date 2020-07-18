import pytest
from django.test import TestCase

from flashcards.leitner.models import Deck, Box, Card, Session
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestLeitnerModelsBasics(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.cl', 'testing321')

    def test_box_creation(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        deck.create_boxes()
        self.assertEqual(Box.objects.filter(deck=deck).count(), 3)

    def test_deck_str_method(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        self.assertEqual(str(deck), 'Test deck')
        self.assertEqual(deck.__str__(), 'Test deck')

    def test_box_str_method(self):
        deck = Deck.objects.create(description='Test deck', created_by=self.user)
        box = Box.objects.create(description='Nothing interesting',
                                 deck=deck, box_type=0)
        self.assertEqual(str(box), 'Box: Nothing interesting | Last used: Never')


# noinspection DuplicatedCode
class TestLeitnerModelsMethods(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.cl', 'testing321')
        self.deck = Deck.objects.create(description='Test deck', created_by=self.user)
        self.deck.create_boxes()
        self.box1 = self.deck.boxes.get(box_type=0)
        self.box2 = self.deck.boxes.get(box_type=1)
        self.box3 = self.deck.boxes.get(box_type=2)

    def test_correct_answer_not_in_last_box(self):
        """ Tests the Card.correct_answer method. Card should go to the next box """
        card = Card.objects.create(
            front_text='Sample card', back_text='Sample card',
            on_deck=self.deck, on_box=self.box1
        )
        session = Session.objects.create(deck=self.deck, current_box=self.box1, total_cards_on_box=1)

        card.correct_answer()

        self.assertEqual(card.on_box, self.box2)
        self.assertNotEqual(card.on_box, self.box1)
        self.assertNotEqual(card.on_box, self.box3)

    def test_correct_answer_in_last_box(self):
        """Tests the Card.correct_answer method when it is on the last box. Card should not move"""
        card = Card.objects.create(
            front_text='Sample card', back_text='Sample card',
            on_deck=self.deck, on_box=self.box3
        )
        session = Session.objects.create(deck=self.deck, current_box=self.box3, total_cards_on_box=1)

        card.correct_answer()

        self.assertEqual(card.on_box, self.box3)
        self.assertNotEqual(card.on_box, self.box1)
        self.assertNotEqual(card.on_box, self.box2)

    def test_wrong_answer(self):
        card = Card.objects.create(
            front_text='Sample card', back_text='Sample card',
            on_deck=self.deck, on_box=self.box3
        )
        session = Session.objects.create(deck=self.deck, current_box=self.box3, total_cards_on_box=1)

        card.wrong_answer()

        self.assertEqual(card.on_box, self.box1)
        self.assertNotEqual(card.on_box, self.box2)
        self.assertNotEqual(card.on_box, self.box3)

    def test_session_current_card_on_empty_box(self):
        """ If you run current_card and the box is empty or there are no cards left, none should be returned"""
        session = Session.objects.create(deck=self.deck, current_box=self.box3, total_cards_on_box=4)
        self.assertIsNone(session.current_card())

    def test_session_current_card(self):
        """Tests the card is returned correctly. Should be the first card added to de box.
           However, modifying a card will move it to the last in the queue"""
        card_defaults = {'front_text': 'Front text', 'back_text': 'Back_text', 'on_deck': self.deck,
                         'on_box': self.box1}
        card1 = Card.objects.create(**card_defaults)
        card2 = Card.objects.create(**card_defaults)
        card3 = Card.objects.create(**card_defaults)
        card4 = Card.objects.create(**card_defaults)

        session = Session.objects.create(deck=self.deck, current_box=self.box1,
                                         total_cards_on_box=self.box1.cards.count())

        self.assertEqual(session.total_cards_on_box, 4)
        self.assertEqual(session.current_card(), card1)
