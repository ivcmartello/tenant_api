from rest_framework import serializers

from users.models import TenantUser


class TenantUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = TenantUser
        fields = ["email", "password", "name"]

    def create(self, validated_data):
        return TenantUser.objects.create_user(is_active=False, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
