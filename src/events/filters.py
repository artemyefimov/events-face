import django_filters

from .models import Event


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Event
        fields = ["name"]
