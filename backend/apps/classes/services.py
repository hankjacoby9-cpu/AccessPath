"""
Every change to who is in a class goes through these functions.

The main rule: a class must always have at least one active professor.
Postgres cannot express that as a simple constraint, so we lock the class's
professor rows, count what would be left, and refuse if the answer is zero.
"""

from django.db import transaction

from .models import Class, ClassMembership

Role = ClassMembership.Role
Status = ClassMembership.Status


class LastProfessorError(Exception):
    """Raised when a change would leave a class with no active professor."""


def create_class(*, user, **fields) -> Class:
    """Create a class. The creator becomes its first professor."""
    with transaction.atomic():
        klass = Class.objects.create(created_by=user, **fields)
        ClassMembership.objects.create(user=user, klass=klass, role=Role.PROFESSOR)
    return klass


def _professors_left_after(membership: ClassMembership, *, new_role=None, new_status=None) -> int:
    # Lock every active professor row in this class so two professors removing
    # each other at the same moment cannot both succeed.
    professors = list(
        ClassMembership.objects.select_for_update()
        .filter(klass_id=membership.klass_id, role=Role.PROFESSOR, status=Status.ACTIVE)
        .values_list("id", flat=True)
    )
    still_professor = (new_role or membership.role) == Role.PROFESSOR and (
        (new_status or membership.status) == Status.ACTIVE
    )
    others = [pk for pk in professors if pk != membership.id]
    return len(others) + (1 if still_professor else 0)


def change_role(membership: ClassMembership, new_role: str) -> ClassMembership:
    with transaction.atomic():
        if _professors_left_after(membership, new_role=new_role) == 0:
            raise LastProfessorError("A class needs at least one professor. Add another professor first.")
        membership.role = new_role
        membership.save(update_fields=["role", "updated_at"])
    return membership


def remove_member(membership: ClassMembership) -> ClassMembership:
    with transaction.atomic():
        if _professors_left_after(membership, new_status=Status.REMOVED) == 0:
            raise LastProfessorError("A class needs at least one professor. Add another professor first.")
        membership.status = Status.REMOVED
        membership.save(update_fields=["status", "updated_at"])
    return membership
