from django.urls import include, path
from rest_framework import routers

from flight_service.views import CrewViewSet, FlightViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "flight"
