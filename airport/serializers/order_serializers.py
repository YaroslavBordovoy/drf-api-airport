from django.db import transaction
from rest_framework import serializers

from airport.models import Order, Ticket
from airport.serializers.ticket_serializers import (
    TicketSerializer,
    TicketListSerializer
)


class OrderSerializer(serializers.ModelSerializer):
    order_tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False
    )

    class Meta:
        model = Order
        fields = ("id", "created_at", "order_tickets")

    @transaction.atomic()
    def create(self, validated_data):
        tickets_data = validated_data.pop("order_tickets")
        order = Order.objects.create(**validated_data)

        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)

        return order


class OrderListSerializer(OrderSerializer):
    order_tickets = TicketListSerializer(many=True, read_only=True)
