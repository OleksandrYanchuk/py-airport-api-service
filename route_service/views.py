from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from airplane.permissions import IsAdminOrIfAuthenticatedReadOnly
from route_service.filters import AirportFilter

from route_service.models import Airport, Route
from route_service.serializers import AirportSerializer, RouteSerializer


class AirportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = AirportPagination
    filterset_class = AirportFilter


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
