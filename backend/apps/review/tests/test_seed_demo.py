import pytest
from django.core.management import call_command

from apps.review.models import Node


@pytest.mark.django_db
def test_seed_demo_runs_twice():
    call_command("seed_demo")
    call_command("seed_demo")
    assert Node.objects.count() == 6
