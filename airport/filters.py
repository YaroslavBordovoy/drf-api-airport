from django.contrib import admin
from django_filters import rest_framework

from airport.models import (
    Flight,
    Crew,
    Route,
    Airport,
    Airplane,
    Ticket,
    Order
)


def custom_filter(field_name: str, lookup_expr: str, current_type: str):
    if current_type == "char":
        field_type = rest_framework.CharFilter
    elif current_type == "date":
        field_type = rest_framework.DateFilter

    return field_type(field_name=field_name, lookup_expr=lookup_expr)


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
    airplane_name = custom_filter(
        field_name="airplane__name",
        lookup_expr="icontains",
        current_type="char")
    departure_airport = custom_filter(
        field_name="route__source__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )
    arrival_airport = custom_filter(
        field_name="route__destination__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )
    departure_time = custom_filter(
        field_name="departure_time",
        lookup_expr="icontains",
        current_type="date"
    )
    arrival_time = custom_filter(
        field_name="arrival_time",
        lookup_expr="icontains",
        current_type="date"
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
    role = custom_filter(
        field_name="role",
        lookup_expr="icontains",
        current_type="char"
    )

    class Meta:
        model = Crew
        fields = ("role",)


class RouteFilter(rest_framework.FilterSet):
    source_city = custom_filter(
        field_name="source__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )
    destination_city = custom_filter(
        field_name="destination__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )

    class Meta:
        model = Route
        fields = ("source_city", "destination_city")


class AirportFilter(rest_framework.FilterSet):
    name = custom_filter(
        field_name="closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )

    class Meta:
        model = Airport
        fields = ("name",)


class AirplaneFilter(rest_framework.FilterSet):
    name = custom_filter(
        field_name="name",
        lookup_expr="icontains",
        current_type="char"
    )
    airplane_type = custom_filter(
        field_name="airplane_type__name",
        lookup_expr="icontains",
        current_type="char"
    )

    class Meta:
        model = Airplane
        fields = ("name", "airplane_type")


class TicketFilter(rest_framework.FilterSet):
    flight_from = custom_filter(
        field_name="flight__route__source__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )
    flight_to = custom_filter(
        field_name="flight__route__destination__closest_big_city",
        lookup_expr="icontains",
        current_type="char"
    )

    class Meta:
        model = Ticket
        fields = ("flight_from", "flight_to")


class OrderFilter(rest_framework.FilterSet):
    created_at = custom_filter(
        field_name="created_at",
        lookup_expr="icontains",
        current_type="date"
    )

    class Meta:
        model = Order
        fields = ("created_at",)
