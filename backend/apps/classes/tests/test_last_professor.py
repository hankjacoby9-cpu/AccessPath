import pytest

from apps.classes import services
from apps.classes.models import ClassMembership

Role = ClassMembership.Role


@pytest.fixture
def klass(make_user):
    prof = make_user("prof@purdue.edu")
    return services.create_class(user=prof, name="Dynamics", course_code="ME 27400")


def test_creator_becomes_professor(klass):
    m = klass.memberships.get()
    assert m.role == Role.PROFESSOR


def test_cannot_remove_last_professor(klass):
    with pytest.raises(services.LastProfessorError):
        services.remove_member(klass.memberships.get())


def test_cannot_demote_last_professor(klass):
    with pytest.raises(services.LastProfessorError):
        services.change_role(klass.memberships.get(), Role.TA)


def test_can_remove_professor_when_another_exists(klass, make_user):
    second = ClassMembership.objects.create(user=make_user("prof2@purdue.edu"), klass=klass, role=Role.PROFESSOR)
    services.remove_member(klass.memberships.exclude(id=second.id).get())
    assert klass.memberships.filter(role=Role.PROFESSOR, status="active").count() == 1


def test_removing_a_ta_is_always_fine(klass, make_user):
    ta = ClassMembership.objects.create(user=make_user("ta@purdue.edu"), klass=klass, role=Role.TA)
    services.remove_member(ta)
    ta.refresh_from_db()
    assert ta.status == "removed"
