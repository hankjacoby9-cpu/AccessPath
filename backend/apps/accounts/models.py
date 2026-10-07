import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class User(AbstractUser):
    """A person who logs in. Email is the login. Role lives on ClassMembership, not here."""

    class TeachingRole(models.TextChoices):
        TEACH = "teach", "I teach a class"
        ASSIST = "assist", "I assist (TA)"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)

    # Purdue verification is planned for week 5. The flag exists now so nothing else changes later.
    purdue_verified = models.BooleanField(default=False)

    # Onboarding answers. These only decide which screen a person sees first.
    onboarding_role = models.CharField(max_length=10, choices=TeachingRole.choices, blank=True)
    onboarding_subject = models.CharField(max_length=200, blank=True)
    onboarding_completed = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
