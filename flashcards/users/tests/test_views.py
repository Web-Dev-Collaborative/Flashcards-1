import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains

from flashcards.users.views import SignupView

pytestmark = pytest.mark.django_db


def test_signup_view_get(rf):
    url = reverse("users:signup")
    request = rf.get(url)
    response = SignupView.as_view()(request)
    assertContains(response, 'Username')
    assertContains(response, 'Password')
    assertContains(response, 'Password confirmation')


def test_signup_view_post_with_valid_form():
    url = reverse("users:signup")
    form = {
        'username': 'ImJustATestingUser',
        'email': 'testinguser@testingserver.com',
        'password1': 'testing321',
        'password2': 'testing321'
    }
    c = Client()
    response = c.post(url, form)
    assert response.status_code == 302


def test_signup_view_post_with_invalid_form():
    url = reverse("users:signup")
    form = {
        'username': 'ImJustATestingUser',
        'email': 'testinguser@testingserver.com',
        'password1': 'apassword',
        'password2': 'adifferentpassword'
    }
    c = Client()
    response = c.post(url, form)
    assert response.status_code == 200
