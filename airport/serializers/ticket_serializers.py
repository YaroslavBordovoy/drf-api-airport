from rest_framework import serializers

from airport.models import Ticket, Flight
from airport.serializers import FlightSerializer, FlightListSerializer


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, attrs):
        row = attrs.get("row")
        seat = attrs.get("seat")
        flight = attrs.get("flight")

        if not flight:
            raise serializers.ValidationError("Flight must be specified.")

        airplane = flight.airplane

        Ticket.validate_ticket(
            row=row,
            seat=seat,
            airplane=airplane,
            error_to_raise=serializers.ValidationError
        )

        return attrs


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

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketDetailSerializer(TicketSerializer):
    flight = serializers.SerializerMethodField()

    def get_flight(self, obj):
        flight_data = FlightListSerializer(obj.flight).data
        flight_data.pop("crew", None)

        return flight_data
