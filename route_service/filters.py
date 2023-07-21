import django_filters

from .models import Airport


class AirportFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.CharFilter(lookup_expr="icontains")
    city = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Airport
        fields = ["country", "state", "city"]
