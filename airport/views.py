from rest_framework import viewsets
from django_filters import rest_framework as filters

from airport.filters import (
    FlightFilter,
    CrewFilter,
    RouteFilter, AirportFilter, AirplaneFilter, TicketFilter, OrderFilter,
)
from airport.models import (
    Flight,
    Crew,
    Route,
    Airport,
    Airplane,
    AirplaneType,
    Ticket,
    Order,
)
from airport.serializers import (
    FlightSerializer,
    FlightDetailSerializer,
    FlightListSerializer,
    CrewSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    RouteListSerializer,
    AirportSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    TicketSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    OrderSerializer,
)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "route",
        "route__source",
        "route__destination",
        "airplane",
        "airplane__airplane_type"
    ).prefetch_related("crew")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CrewFilter


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneFilter


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        "flight",
        "order__user",
        "flight__route",
        "flight__airplane",
        "flight__route__source",
        "flight__route__destination",
    ).prefetch_related(
        "flight__crew",
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TicketFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer

        if self.action == "retrieve":
            return TicketDetailSerializer

        return TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("order_tickets")
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
