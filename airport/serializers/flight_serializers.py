from rest_framework import serializers

from airport.models import Flight
from airport.serializers.route_serializers import RouteDetailSerializer
from airport.serializers.airplane_serializers import AirplaneSerializer
from airport.serializers.crew_serializers import CrewSerializer


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )

    def validate(self, attrs):
        crew_data = attrs.pop("crew", None)
        flight = Flight(**attrs)

        try:
            flight.clean()
        except ValueError:
            raise serializers.ValidationError

        return attrs


class FlightListSerializer(serializers.ModelSerializer):
    departure_airport = serializers.CharField(
        source="route.source.name",
        read_only=True
    )
    arrival_airport = serializers.CharField(
        source="route.destination.name",
        read_only=True
    )
    airplane_name = serializers.CharField(
        source="airplane.name",
        read_only=True
    )
    airplane_type = serializers.CharField(
        source="airplane.airplane_type",
        read_only=True
    )
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "departure_airport",
            "arrival_airport",
            "airplane_name",
            "airplane_type",
            "departure_time",
            "arrival_time",
            "crew",
            "tickets_available"
        )


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer()
    airplane = AirplaneSerializer()
    crew = CrewSerializer(many=True, read_only=True)
    taken_seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="seat",
        source="flight_tickets"
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_seats"
        )
