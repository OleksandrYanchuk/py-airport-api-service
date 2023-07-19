from django.urls import include, path
from rest_framework import routers

from airplane.views import AirplaneTypeViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register("airplane_type", AirplaneTypeViewSet)


router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airplane"
