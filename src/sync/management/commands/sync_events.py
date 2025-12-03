from datetime import datetime

from django.core.management.base import BaseCommand

from core.settings import EVENTS_PROVIDER_ACCESS_TOKEN, EVENTS_PROVIDER_URL
from sync.client import EventsProviderClient
from sync.services import sync_events


class Command(BaseCommand):
    help = "Synchronize events from events-provider"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all", action="store_true", help="Synchronize all events (full sync)"
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Synchronize events changed from this date (YYYY-MM-DD)",
        )

    def handle(self, *args, **options):
        full_sync = options["all"]
        date_str = options.get("date")
        from_date = datetime.fromisoformat(date_str) if date_str else None

        client = EventsProviderClient(
            base_url=EVENTS_PROVIDER_URL,  # type: ignore
            access_token=EVENTS_PROVIDER_ACCESS_TOKEN,  # type: ignore
        )

        new_count, updated_count = sync_events(
            client, full_sync=full_sync, from_date=from_date
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync finished. New: {new_count}, Updated: {updated_count}"
            )
        )
