from rest_framework import serializers

from accounts.serializers import UserSerializer
from airport.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class OrderListSerializer(OrderSerializer):
    user = UserSerializer()
