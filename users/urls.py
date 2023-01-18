from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomAuthToken, TenantUserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("tenantuser", TenantUserViewSet, basename="tenantusers")

urlpatterns = [
    path("api-auth-token/", CustomAuthToken.as_view()),
    path("", include(router.urls))
]
