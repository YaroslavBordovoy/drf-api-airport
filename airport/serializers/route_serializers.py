from rest_framework import serializers

from airport.models import Route
from airport.serializers import AirportSerializer


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")
        read_only_fields = ("id", "distance")

    def create(self, validated_data):
        route = Route(**validated_data)
        route.clean()
        route.save()

        return route


class RouteListSerializer(RouteSerializer):
    source_city = serializers.CharField(
        source="source.closest_big_city",
        read_only=True
    )
    destination_city = serializers.CharField(
        source="destination.closest_big_city",
        read_only=True
    )

    class Meta:
        model = Route
        fields = ("id", "source_city", "destination_city", "distance")
        read_only_fields = ("id", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()
