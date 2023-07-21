from django.urls import include, path
from rest_framework import routers

from route_service.views import AirportViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "route"
