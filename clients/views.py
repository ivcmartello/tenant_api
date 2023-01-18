import logging

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.models import Client
from clients.serializers import ClientSerializer

logger = logging.getLogger(__name__)


class ClientViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def retrieve(self, request, pk):
        queryset = Client.objects.filter(uuid=pk).first()
        serializer = self.serializer_class(queryset, context={"request": request})
        return Response(serializer.data)

    def list(self, request):
        queryset = Client.objects.all()
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def update(self, request, pk):
        data = {
            "uuid": pk,
            "name": request.data.get("name"),
            "document": request.data.get("document"),
        }

        serializer = self.serializer_class(
            data=data,
            context={
                "request": request
            },
        )

        try:
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                instance = Client.objects.filter(uuid=pk).first()
                serializer.update(instance, serializer.validated_data)
        except Exception as exception:
            logger.error(f"{exception}")
            return Response(f"{exception}", status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
