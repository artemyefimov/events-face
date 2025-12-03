from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from events.models import Event

from .filters import EventFilter
from .pagination import EventCursorPagination
from .serializers import EventSerializer


class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.select_related("place")
    serializer_class = EventSerializer
    pagination_class = EventCursorPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = EventFilter
    # search_fields = ["name"]
    # ordering_fields = ["event_time"]
    ordering = ["event_time"]
    # permission_classes = [permissions.IsAuthenticated]
