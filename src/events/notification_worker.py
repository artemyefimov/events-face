import time

import requests
from django.db import transaction

from .models import RegistrationNotification


class NotificationWorker:
    def __init__(self, notification_client, batch_size=100, idle_sleep=10):
        self.client = notification_client
        self.batch_size = batch_size
        self.idle_sleep = idle_sleep
        self._running = False

    def fetch_batch(self):
        with transaction.atomic():
            qs = (
                RegistrationNotification.objects.select_for_update(skip_locked=True)
                .filter(is_sent=False)
                .select_related("registration")[: self.batch_size]
            )
            return list(qs)

    def process_batch(self):
        notifications = self.fetch_batch()
        if not notifications:
            return 0

        successful = []

        for notification in notifications:
            try:
                registration = notification.registration
                email = registration.email
                message = f"Registration notification for {registration.id}"

                self.client.send_notification(
                    id=str(notification.id),
                    message=message,
                    email=email,
                )

                successful.append(notification.id)

            except requests.exceptions.HTTPError:
                continue

        if successful:
            RegistrationNotification.objects.filter(id__in=successful).update(
                is_sent=True
            )

        return len(successful)

    def run(self):
        self._running = True

        while self._running:
            processed = self.process_batch()

            if processed == 0:
                time.sleep(self.idle_sleep)

    def stop(self):
        self._running = False
