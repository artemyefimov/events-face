import secrets

from django.db import transaction
from rest_framework import serializers

from .models import Event, Registration, RegistrationNotification


class EventSerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "event_time",
            "status",
            "place_name",
        ]

    def get_place_name(self, obj) -> str | None:
        if obj.place is not None:
            return obj.place.name
        return None


class RegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["full_name", "email"]

    def validate(self, attrs):
        event = self.context["event"]
        if event.status != Event.Status.OPEN:
            raise serializers.ValidationError({"event": "Registration is closed"})
        return attrs

    def create(self, validated_data):
        event = self.context["event"]

        with transaction.atomic():
            registration = Registration.objects.create(
                event=event,
                full_name=validated_data["full_name"],
                email=validated_data["email"],
                confirmation_code=secrets.token_hex(8),
            )

            RegistrationNotification.objects.create(
                registration=registration,
            )

        return registration
