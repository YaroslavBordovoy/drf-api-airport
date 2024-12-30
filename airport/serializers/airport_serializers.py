from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")
        validators = [
            UniqueTogetherValidator(
                queryset=Airport.objects.all(),
                fields=("name", "closest_big_city"),
                message="Airport with this name and city already exists."
            )
        ]

    def validate(self, attrs):
        airport = Airport(**attrs)

        try:
            airport.clean()
        except ValueError:
            raise serializers.ValidationError

        return attrs
