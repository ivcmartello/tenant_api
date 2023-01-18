import logging
from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.models import Client
from events.models import Event
from events.serializers import EventSerializer

# Create your views here.

logger = logging.getLogger(__name__)


class EventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def create(self, request):
        event = request.data or {}
        created_by = Client.objects.get(uuid=request.META.get("HTTP_X_REQUEST_ID"))
        serializer_context = {"created_by": created_by}
        serializer = self.serializer_class(data=event, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        event = Event.objects.filter(pk=pk).first()
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)

        event_data = request.data or {}
        serializer = self.serializer_class(event, data=event_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        pass

    def list(self, request):
        queryset = Event.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        event = Event.objects.filter(pk=pk).first()
        if not event:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event.cancelled_at = datetime.now()
        event.save()

        return Response(status=status.HTTP_200_OK)
