import pytest
from pytest_django.asserts import assertContains
from django.test import RequestFactory, TestCase

from flashcards.users.models import User
from flashcards.users.views import LoginView

pytestmark = pytest.mark.django_db


def test_login_view_get(rf):
    # Covers the get method of LoginView
    request = rf.get('/account/login')
    callable_obj = LoginView.as_view()
    response = callable_obj(request)
    assertContains(response, 'Username')
    assertContains(response, 'Password')
