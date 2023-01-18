from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet

router = DefaultRouter(trailing_slash=False)
router.register("event", EventViewSet, basename="events")

urlpatterns = [
    path("", include(router.urls)),
]
