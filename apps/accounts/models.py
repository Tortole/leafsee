"""
Module with models for user and relationships between them
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class LeafseeUser(AbstractUser):
    """
    Model for user

    Fields:
        username - CharField - username
        password - - user password
        first_name - CharField - user first name
        last_name - CharField - user last name
        email - EmailField - user e-mail
        nickname - CharField - Public showing username, it can be non unique

    Notes:
        Super AbstractUser class include field:
            username    | CharField     | max_length=150, unique=True
            first_name  | CharField     | max_length=150, blank=True
            last_name   | CharField     | max_length=150, blank=True
            email       | EmailField    | blank=True
    """

    nickname = models.CharField(max_length=100)
    subscriptions = models.ManyToManyField(
        "self",
        through="Subscriptions",
        through_fields=("subscriber", "content_creator"),
    )


class Subscriptions(models.Model):
    """
    Model for tracking subscriptions

    Fields:
        subscriber - ForeignKey - who subscribed
        content_creator - ForeignKey - subscribed to
        subscriptions_date - DateField - date of subscriptions

    Notes:
        Every model instance unique by subscriber and content_creator
    """

    subscriber = models.ForeignKey(
        LeafseeUser, related_name="subscriber", on_delete=models.CASCADE
    )
    content_creator = models.ForeignKey(
        LeafseeUser, related_name="content_creator", on_delete=models.CASCADE
    )
    subscriptions_date = models.DateField()

    class Meta:
        # Unique pair of subscriber and content_creator
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "content_creator"], name="unique_subscriptions"
            )
        ]
