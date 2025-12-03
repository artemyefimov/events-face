from django.db import models


class SyncLog(models.Model):
    run_at = models.DateTimeField(auto_now_add=True)
    new_events_count = models.PositiveIntegerField(default=0)
    updated_events_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-run_at"]
