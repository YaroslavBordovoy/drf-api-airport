from django_filters import rest_framework
from django.contrib import admin

from airport.models import (
    Flight,
    Crew,
    Route,
    Airport,
    Airplane,
    Ticket,
    Order
)


class DistanceRangeFilterAdmin(admin.SimpleListFilter):
    title = "Distance Range"
    parameter_name = "distance_range"

    def lookups(self, request, model_admin):
        return [
            ("short", "0-2000 km"),
            ("medium", "2001-5000 km"),
            ("long", ">5001 km"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "short":
            return queryset.filter(distance__lte=2000)
        elif self.value() == "medium":
            return queryset.filter(distance__gt=2000, distance__lte=5000)
        elif self.value() == "long":
            return queryset.filter(distance__gte=5001)

        return queryset


class FlightFilter(rest_framework.FilterSet):
    airplane_name = rest_framework.CharFilter(
        field_name="airplane__name",
        lookup_expr="icontains"
    )
    departure_airport = rest_framework.CharFilter(
        field_name="route__source__closest_big_city",
        lookup_expr="icontains"
    )
    arrival_airport = rest_framework.CharFilter(
        field_name="route__destination__closest_big_city",
        lookup_expr="icontains"
    )
    departure_time = rest_framework.DateFilter(
        field_name="departure_time",
        lookup_expr="icontains"
    )
    arrival_time = rest_framework.DateFilter(
        field_name="arrival_time",
        lookup_expr="icontains"
    )

    class Meta:
        model = Flight
        fields = (
            "airplane_name",
            "departure_airport",
            "arrival_airport",
            "departure_time",
            "arrival_time"
        )


class CrewFilter(rest_framework.FilterSet):
    role = rest_framework.CharFilter(
        field_name="role",
        lookup_expr="icontains"
    )

    class Meta:
        model = Crew
        fields = ("role",)


class RouteFilter(rest_framework.FilterSet):
    source_city = rest_framework.CharFilter(
        field_name="source__closest_big_city",
        lookup_expr="icontains"
    )
    destination_city = rest_framework.CharFilter(
        field_name="destination__closest_big_city",
        lookup_expr="icontains"
    )

    class Meta:
        model = Route
        fields = ("source_city", "destination_city")


class AirportFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name="closest_big_city",
        lookup_expr="icontains"
    )

    class Meta:
        model = Airport
        fields = ("name",)


class AirplaneFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )
    airplane_type = rest_framework.CharFilter(
        field_name="airplane_type__name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Airplane
        fields = ("name", "airplane_type")


class TicketFilter(rest_framework.FilterSet):
    flight_from = rest_framework.CharFilter(
        field_name="flight__route__source__closest_big_city",
        lookup_expr="icontains"
    )
    flight_to = rest_framework.CharFilter(
        field_name="flight__route__destination__closest_big_city",
        lookup_expr="icontains"
    )

    class Meta:
        model = Ticket
        fields = ("flight_from", "flight_to")


class OrderFilter(rest_framework.FilterSet):
    created_at = rest_framework.DateFilter(
        field_name="created_at",
        lookup_expr="icontains"
    )

    class Meta:
        model = Order
        fields = ("created_at",)
