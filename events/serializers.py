from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(required=False)
    title = serializers.CharField()

    class Meta:
        model = Event
        fields = ["id", "title"]

    def create(self, validated_data):
        created_by = self.context.get("created_by", None)
        return Event.objects.create(created_by=created_by, **validated_data)
