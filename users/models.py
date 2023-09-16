from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Add additional fields in here
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )

    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
    )

    groups = models.ManyToManyField(Group, blank=False, related_name="user_set")

    def __str__(self):
        return self.username
