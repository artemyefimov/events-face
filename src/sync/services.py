from django.db import transaction

from events.models import Event, Place
from sync.client import EventsProviderClient

from .models import SyncLog


def _transform_status(status):
    match status:
        case "new", "published":
            return "open"
        case "registration_closed", "finished", "cancelled":
            return "closed"


def sync_events(client: EventsProviderClient, full_sync=False, from_date=None):
    data = client.get_events(changed_at=None if full_sync else from_date)

    new_count = 0
    updated_count = 0

    with transaction.atomic():
        for item in data:
            place = None
            place_data = item.get("place")

            if place_data:
                place, _ = Place.objects.update_or_create(
                    id=place_data["id"],
                    defaults={
                        "name": place_data["name"],
                    },
                )

            _, new = Event.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "event_time": item["event_time"],
                    "registration_deadline": item["registration_deadline"],
                    "status": _transform_status(item["status"]),
                    "place": place,
                },
            )

            if new:
                new_count += 1
            else:
                updated_count += 1

        SyncLog.objects.create(
            new_events_count=new_count, updated_events_count=updated_count
        )

    return new_count, updated_count
