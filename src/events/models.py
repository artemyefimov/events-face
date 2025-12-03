from uuid import uuid4

from django.db import models


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)


class Event(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=8, choices=Status.choices, db_index=True)
    place = models.ForeignKey(
        Place, on_delete=models.SET_NULL, related_name="events", null=True, blank=True
    )
    event_time = models.DateTimeField(db_index=True)


class Registration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )

    full_name = models.CharField(max_length=128)

    email = models.EmailField()

    confirmation_code = models.CharField(max_length=8)

    class Meta:
        unique_together = ["event", "email"]


class RegistrationNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    registration = models.ForeignKey(
        Registration,
        on_delete=models.DO_NOTHING,
        related_name="notifications",
    )

    is_sent = models.BooleanField(default=False)
