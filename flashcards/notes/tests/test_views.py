from datetime import datetime

import pytest
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse

from flashcards.notes.models import Note
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestFlashcardViewsIncludingCreator(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user1 = User.objects.create_user('test_username', 'testmail@example.com', 'testing321')
        self.user2 = User.objects.create_user('test_username2', 'testmail2@example.com', 'testing321')
        self.note = Note.objects.create(title='Sample title for user1', content='Sample content',
                                        created_by=self.user1)

    def test_create_flash_includes_creator(self):
        """ Tests that creating a flashcard adds the user to the database """
        form = {
            'title': 'Sample title',
            'content': 'Some random content'
        }
        self.client.force_login(self.user1)
        self.client.post(reverse("notes:create"), form)
        assert Note.objects.last().created_by == self.user1

    def test_get_queryset_on_detail_view_with_intended_user(self):
        """ Tests the get_queryset method on NoteDetailView
         should only include flashcards made by the user.
         Should get a http code 200"""
        self.client.force_login(self.user1)
        url = self.note.get_absolute_url()
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_queryset_on_detail_view_with_unintended_user(self):
        """ If a user who is not the creator of the card tries to access it, the user should
        get a 404 error"""
        self.client.force_login(self.user2)
        url = self.note.get_absolute_url()
        response = self.client.get(url)
        assert response.status_code == 404
