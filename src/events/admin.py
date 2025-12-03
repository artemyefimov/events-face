from django.contrib import admin

from .models import Event, Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_time", "status", "place")
    list_filter = ("status", "event_time", "place")
    search_fields = ("name",)
    ordering = ("event_time",)
    readonly_fields = ("id",)
