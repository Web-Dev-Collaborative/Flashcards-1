import pytest
from django.test import TestCase, Client
from django.urls import reverse

from flashcards.leitner.models import Deck, Box, Card
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestDeckRelatedViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')

    def test_deck_list_view_get(self):
        """ If the user is logged in, page should load correctly """
        url = reverse('leitner:deck-list')
        self.client.force_login(self.user)

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_deck_list_view_post_valid_form(self):
        """ Asserts the deck was created successfully after a valid form """
        url = reverse('leitner:deck-list')
        self.client.force_login(self.user)
        data = {'description': 'This is a test deck that was created for testing purposes'}
        last_deck_before = Deck.objects.last()

        self.client.post(url, data=data)  # This should be a valid post
        deck = Deck.objects.get(description=data['description'], created_by=self.user)

        self.assertEquals(Deck.objects.last(), deck)
        self.assertNotEqual(last_deck_before, deck)

    def test_deck_list_view_post_invalid_form(self):
        """ Asserts a deck wasn't created given an invalid form """
        url = reverse('leitner:deck-list')
        self.client.force_login(self.user)
        data = {'description': ''}
        deck_before = Deck.objects.last()

        self.client.post(url, data=data)
        deck_after = Deck.objects.last()

        self.assertEquals(deck_before, deck_after)

    def test_deck_detail_view(self):
        deck = Deck.objects.create(description='blah', created_by=self.user)
        url = reverse('leitner:deck-detail', args=(deck.pk,))
        self.client.force_login(self.user)

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_deck_delete_view_qs(self):
        deck = Deck.objects.create(description='Something not important', created_by=self.user)
        another_user = User.objects.create_user('anotheruser', 'b@b.com', 'testing321')
        self.client.force_login(another_user)
        delete_url = reverse('leitner:deck-delete', args=(deck.pk,))

        response = self.client.get(delete_url)

        self.assertEquals(response.status_code, 404)


# noinspection DuplicatedCode
class TestCardRelatedViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')
        self.client.force_login(self.user)
        self.deck = Deck.objects.create(description='Nothing important', created_by=self.user)

    def test_card_creation_view_get(self):
        url = reverse('leitner:add-card', args=(self.deck.pk,))

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_card_creation_view_post_valid_form(self):
        url = reverse('leitner:add-card', args=(self.deck.pk,))
        box = Box.objects.create(description='Box', deck=self.deck, box_type=0)
        data = {'front_text': 'Front text', 'back_text': 'Back text', 'on_box': box.pk}

        last_card_before = Card.objects.last()
        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertNotEqual(last_card_before, new_card)

    def test_card_creation_view_post_invalid_form(self):
        url = reverse('leitner:add-card', args=(self.deck.pk,))
        data = {'front_text': 'Front text', 'back_text': 'Back text', 'on_box': ''}

        last_card_before = Card.objects.last()
        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertEqual(last_card_before, new_card)

    def test_card_update_view_get(self):
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', args=(self.deck.pk, card.pk))

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_card_update_view_post_valid_form(self):
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', kwargs={'deck_pk': self.deck.pk, 'card_pk': card.pk})
        data = {'front_text': 'After change', 'back_text': 'After change'}

        self.client.post(url, data=data)
        new_card = Card.objects.last()

        card.refresh_from_db()
        self.assertEquals(card, new_card)
        self.assertEquals(card.front_text, 'After change')
        self.assertEquals(card.back_text, 'After change')

    def test_card_update_view_post_invalid_form(self):
        box = Box.objects.create(description='..', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='No change', back_text='No change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', kwargs={'deck_pk': self.deck.pk, 'card_pk': card.pk})
        data = {'front_text': '', 'back_text': ''}

        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertEquals(card, new_card)
        self.assertEquals(card.front_text, 'No change')
        self.assertEquals(card.back_text, 'No change')

    def test_card_delete_view_get(self):
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-delete', args=(self.deck.pk, card.pk))

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    # noinspection PyTypeChecker
    def test_card_delete_view_post(self):
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-delete', args=(self.deck.pk, card.pk))

        self.client.post(url)

        self.assertRaises(Card.DoesNotExist, card.refresh_from_db)
#
#
# class TestSessionRelatedViews(TestCase):
#
#     def setUp(self) -> None:
#         self.client = Client()
#         self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')
#
#     def test_session_start_view(self):
#         pass
#
#     def test_session_cards_view(self):
#         pass
#
#     def test_session_finished_view(self):
#         pass
