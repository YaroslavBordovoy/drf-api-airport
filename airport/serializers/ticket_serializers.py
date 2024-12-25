from rest_framework import serializers

from airport.models import Ticket, Flight
from airport.serializers import FlightSerializer, OrderSerializer, FlightListSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketFlightSerializer(FlightSerializer):
    route = serializers.CharField(
        source="route.route",
        read_only=True
    )
    airplane = serializers.CharField(
        source="airplane.name",
        read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class TicketListSerializer(serializers.ModelSerializer):
    flight = TicketFlightSerializer()
    order = serializers.CharField(source="order.user", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketDetailSerializer(TicketSerializer):
    flight = FlightListSerializer()
    order = OrderSerializer()