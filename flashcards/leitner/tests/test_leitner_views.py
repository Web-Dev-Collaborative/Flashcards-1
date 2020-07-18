import pytest
from django.test import TestCase, Client
from django.urls import reverse

from flashcards.leitner.models import Deck, Box, Card, Session
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

        self.assertEqual(response.status_code, 200)

    def test_deck_list_view_post_valid_form(self):
        """ Asserts the deck was created successfully after a valid form """
        url = reverse('leitner:deck-list')
        self.client.force_login(self.user)
        data = {'description': 'This is a test deck that was created for testing purposes'}
        last_deck_before = Deck.objects.last()

        self.client.post(url, data=data)  # This should be a valid post
        deck = Deck.objects.get(description=data['description'], created_by=self.user)

        self.assertEqual(Deck.objects.last(), deck)
        self.assertNotEqual(last_deck_before, deck)

    def test_deck_list_view_post_invalid_form(self):
        """ Asserts a deck wasn't created given an invalid form """
        url = reverse('leitner:deck-list')
        self.client.force_login(self.user)
        data = {'description': ''}
        deck_before = Deck.objects.last()

        self.client.post(url, data=data)
        deck_after = Deck.objects.last()

        self.assertEqual(deck_before, deck_after)

    def test_deck_detail_view(self):
        deck = Deck.objects.create(description='blah', created_by=self.user)
        url = reverse('leitner:deck-detail', args=(deck.pk,))
        self.client.force_login(self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_deck_delete_view_qs(self):
        deck = Deck.objects.create(description='Something not important', created_by=self.user)
        another_user = User.objects.create_user('anotheruser', 'b@b.com', 'testing321')
        self.client.force_login(another_user)
        delete_url = reverse('leitner:deck-delete', args=(deck.pk,))

        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 404)


# noinspection DuplicatedCode
class TestCardRelatedViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')
        self.client.force_login(self.user)
        self.deck = Deck.objects.create(description='Nothing important', created_by=self.user)

    def test_card_creation_view_get(self):
        """ Asserts the get method works """
        url = reverse('leitner:add-card', args=(self.deck.pk,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_card_creation_view_post_valid_form(self):
        """ Asserts a card is correctly created given a valid form"""
        url = reverse('leitner:add-card', args=(self.deck.pk,))
        box = Box.objects.create(description='Box', deck=self.deck, box_type=0)
        data = {'front_text': 'Front text', 'back_text': 'Back text', 'on_box': box.pk}

        last_card_before = Card.objects.last()
        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertNotEqual(last_card_before, new_card)

    def test_card_creation_view_post_invalid_form(self):
        """ Asserts a card is not created when submitting an invalid form """
        url = reverse('leitner:add-card', args=(self.deck.pk,))
        data = {'front_text': 'Front text', 'back_text': 'Back text', 'on_box': ''}

        last_card_before = Card.objects.last()
        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertEqual(last_card_before, new_card)

    def test_card_update_view_get(self):
        """ Asserts the get method works correctly """
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', args=(self.deck.pk, card.pk))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_card_update_view_post_valid_form(self):
        """ Asserts the card is modified correctly after a valid post """
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', kwargs={'deck_pk': self.deck.pk, 'card_pk': card.pk})
        data = {'front_text': 'After change', 'back_text': 'After change'}

        self.client.post(url, data=data)
        new_card = Card.objects.last()

        card.refresh_from_db()
        self.assertEqual(card, new_card)
        self.assertEqual(card.front_text, 'After change')
        self.assertEqual(card.back_text, 'After change')

    def test_card_update_view_post_invalid_form(self):
        """ Asserts the card is not modified after an invalid post """
        box = Box.objects.create(description='..', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='No change', back_text='No change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-update', kwargs={'deck_pk': self.deck.pk, 'card_pk': card.pk})
        data = {'front_text': '', 'back_text': ''}

        self.client.post(url, data=data)
        new_card = Card.objects.last()

        self.assertEqual(card, new_card)
        self.assertEqual(card.front_text, 'No change')
        self.assertEqual(card.back_text, 'No change')

    def test_card_delete_view_get(self):
        """ Asserts the get method works """
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-delete', args=(self.deck.pk, card.pk))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # noinspection PyTypeChecker
    def test_card_delete_view_post(self):
        """ Asserts the card is deleted """
        box = Box.objects.create(description='...', deck=self.deck, box_type=0)
        card = Card.objects.create(front_text='Before change', back_text='Before change',
                                   on_deck=self.deck, on_box=box)
        url = reverse('leitner:card-delete', args=(self.deck.pk, card.pk))

        self.client.post(url)

        self.assertRaises(Card.DoesNotExist, card.refresh_from_db)


# noinspection DuplicatedCode
class TestSessionRelatedViews(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')
        self.client = Client()
        self.client.force_login(self.user)

        self.deck = Deck.objects.create(description='Test deck', created_by=self.user)
        self.deck.create_boxes()

        self.box1 = self.deck.boxes.get(box_type=0)
        self.box2 = self.deck.boxes.get(box_type=1)
        self.box3 = self.deck.boxes.get(box_type=2)

        for i in range(10):
            Card.objects.create(front_text=f'Card {i} front text', back_text=f'Card {i} back text',
                                on_deck=self.deck, on_box=self.box1)

        self.start_session_url = reverse('leitner:session', args=(self.deck.pk,))
        self.study_session_url = reverse('leitner:session-cards', args=(self.deck.pk,))
        self.session_finished_url = reverse('leitner:session-finished', args=(self.deck.pk,))

    # GET method tests

    def test_session_redirects_when_session_exists(self):
        """ """
        session = Session.objects.create(deck=self.deck, current_box=self.box1,
                                         total_cards_on_box=10, is_finished=False)

        response = self.client.get(self.start_session_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.session_finished_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.study_session_url)
        self.assertEqual(response.status_code, 200)

    def test_session_redirect_when_session_does_not_exist(self):
        response = self.client.get(self.start_session_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.session_finished_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.study_session_url)
        self.assertEqual(response.status_code, 302)

    def test_session_redirect_when_session_finished(self):
        session = Session.objects.create(deck=self.deck, current_box=self.box1,
                                         total_cards_on_box=10, is_finished=True)

        response = self.client.get(self.start_session_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.session_finished_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.study_session_url)
        self.assertEqual(response.status_code, 302)

    # POST method tests

    def test_session_start_view_post_with_valid_form(self):
        pass

    def test_session_start_view_with_invalid_form(self):
        pass

    def test_session_cards_view_with_correct_answer_post(self):
        pass

    def test_session_cards_view_with_incorrect_answer_post(self):
        pass

    def test_session_cards_view_with_invalid_post(self):
        pass

    def test_session_finished_view_post_method(self):
        pass
