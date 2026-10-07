import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.fixture
def make_user(db):
    def make(email="prof@purdue.edu", password="a-good-password-123"):
        return User.objects.create_user(email=email, password=password)
    return make


@pytest.fixture
def api():
    return APIClient()
