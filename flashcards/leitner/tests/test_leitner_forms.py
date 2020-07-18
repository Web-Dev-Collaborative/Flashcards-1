import pytest
from django.test import TestCase

from flashcards.leitner.forms import CardCreationForm, SessionSelectBoxForm
from flashcards.leitner.models import Deck
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestLeitnerForms(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('testuser', 'a@a.com', 'testing321')
        self.deck = Deck.objects.create(description='Desc', created_by=self.user)
        self.deck.create_boxes()
        self.boxes = self.deck.boxes.get(box_type=0), self.deck.boxes.get(box_type=1), self.deck.boxes.get(box_type=2)

    def test_card_creation_form(self):
        form = CardCreationForm(self.deck)

        for idx, box in enumerate(self.boxes):
            self.assertEqual(box, form.fields['on_box'].queryset[idx])

    def test_session_select_box_form(self):
        form = SessionSelectBoxForm(self.deck)

        for idx, box in enumerate(self.boxes):
            self.assertEqual(box, form.fields['current_box'].queryset[idx])
