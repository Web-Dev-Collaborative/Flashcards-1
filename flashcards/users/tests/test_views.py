import pytest
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertContains

from flashcards.users.views import SignupView

pytestmark = pytest.mark.django_db


class TestSignUpview(TestCase):
    def setUp(self):
        self.url = reverse("users:signup")
        self.client = Client()
        self.factory = RequestFactory()

    def test_signup_view_get(self):
        response = SignupView.as_view()(self.factory.get(self.url))
        assertContains(response, 'Username')
        assertContains(response, 'Password')
        assertContains(response, 'Password confirmation')

    def test_signup_view_post_with_valid_form(self):
        form = {
            'username': 'ImJustATestingUser',
            'email': 'testinguser@testingserver.com',
            'password1': 'testing321',
            'password2': 'testing321'
        }
        response = self.client.post(self.url, form)
        assert response.status_code == 302

    def test_signup_view_post_with_invalid_form(self):
        form = {
            'username': 'ImJustATestingUser',
            'email': 'testinguser@testingserver.com',
            'password1': 'apassword',
            'password2': 'adifferentpassword'
        }
        response = self.client.post(self.url, form)
        assert response.status_code == 200
