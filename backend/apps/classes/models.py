from django.conf import settings
from django.db import models

from apps.common import BaseModel


class Class(BaseModel):
    """A course a professor creates. Every file and node belongs to exactly one class."""

    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, blank=True)
    course_code = models.CharField(max_length=50, blank=True)  # "ME 27400"
    term = models.CharField(max_length=50, blank=True)  # "Fall 2026"
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name="created_classes")

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return f"{self.course_code} {self.name}".strip()

    @property
    def s3_prefix(self):
        return f"classes/{self.id}/"


class ClassMembership(BaseModel):
    """Says one person is a professor or TA in one class. This is the real permission."""

    class Role(models.TextChoices):
        PROFESSOR = "professor", "Professor"
        TA = "ta", "TA"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REMOVED = "removed", "Removed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name="+")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "klass"], name="one_membership_per_class")]

    def __str__(self):
        return f"{self.user} is {self.role} in {self.klass}"


class Invite(BaseModel):
    """An emailed invitation to join a class with a given role."""

    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="invites")
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ClassMembership.Role.choices)
    token_hash = models.CharField(max_length=64, unique=True)  # sha256 of the token, never the token itself
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)


class Lecture(BaseModel):
    """A lecture inside a class. The TA writes ta_context to help the AI."""

    klass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    ta_context = models.TextField(blank=True, help_text="What this lecture covers and what students should take away.")

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return self.title
