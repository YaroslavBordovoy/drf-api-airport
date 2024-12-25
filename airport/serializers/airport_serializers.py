from rest_framework import serializers

from airport.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")

    def validate(self, attrs):
        airport = Airport(**attrs)

        try:
            airport.clean()
        except ValueError:
            raise serializers.ValidationError

        return attrs
