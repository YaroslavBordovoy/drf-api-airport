from rest_framework import serializers

from airport.models import Airplane


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.StringRelatedField()
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "capacity",
            "image"
        )
        read_only_fields = ("id", "airplane_type")
