from django.contrib.auth import get_user_model
from django_tenants.utils import get_public_schema_name, schema_context
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import TenantUserSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        tenants = [
            {"uuid": v["uuid"], "name": v["name"]} for v in user.tenants.values()
        ]
        userdata = {
            "name": user.name,
            "email": user.email,
            "tenants": tenants,
        }
        return Response({"token": token.key, "user": userdata})


class TenantUserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = TenantUserSerializer

    def create(self, request):
        tenantuser = request.data or {}

        with schema_context(get_public_schema_name()):
            user = (
                get_user_model()
                .objects.filter(email__exact=tenantuser["email"])
                .first()
            )

            if not user:
                serializer = self.serializer_class(data=tenantuser)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user = get_user_model().objects.get(email__exact=tenantuser["email"])
                
                # Just for example
                user.is_active = True
                user.is_verified = True
                user.save()
                
                return Response("OK", status=status.HTTP_201_CREATED)

            return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        users = get_user_model().objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        pass
