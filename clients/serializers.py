from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    document = serializers.CharField()

    class Meta:
        model = Client
        fields = ["uuid", "name", "document"]

