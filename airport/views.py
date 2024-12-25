from django.db.models import Count, F
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from airport.filters import (
    FlightFilter,
    CrewFilter,
    RouteFilter,
    AirportFilter,
    AirplaneFilter,
    TicketFilter,
    OrderFilter
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
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.schema_params import (
    FLIGHT_LIST_PARAMETERS,
    CREW_LIST_PARAMETERS,
    ROUTE_LIST_PARAMETERS,
    AIRPORT_LIST_PARAMETERS,
    AIRPLANE_LIST_PARAMETERS,
    TICKET_LIST_PARAMETERS,
    ORDER_LIST_PARAMETERS
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
    OrderListSerializer,
)


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FlightFilter

    def get_queryset(self):
        self.queryset = Flight.objects.select_related(
            "route",
            "route__source",
            "route__destination",
            "airplane",
            "airplane__airplane_type"
        ).prefetch_related("crew")

        if self.action == "list":
            return self.queryset.annotate(
                tickets_available=F("airplane__rows")
                * F("airplane__seats_in_row")
                - Count("flight_tickets")
            ).order_by("id")

        return self.queryset

    @extend_schema(
        parameters=FLIGHT_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of flights"""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CrewFilter

    @extend_schema(
        parameters=CREW_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of crews"""
        return super().list(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RouteFilter

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer

    @extend_schema(
        parameters=ROUTE_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of routes"""
        return super().list(request, *args, **kwargs)

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirportFilter

    @extend_schema(
        parameters=AIRPORT_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of airports"""
        return super().list(request, *args, **kwargs)

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AirplaneFilter

    @extend_schema(
        parameters=AIRPLANE_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of airplanes"""
        return super().list(request, *args, **kwargs)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TicketFilter

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer

        if self.action == "retrieve":
            return TicketDetailSerializer

        return TicketSerializer

    @extend_schema(
        parameters=TICKET_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of tickets"""
        return super().list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user").prefetch_related(
        "order_tickets__flight__route__source",
        "order_tickets__flight__route__destination",
        "order_tickets__flight__airplane",
    )
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer

        return OrderSerializer

    @extend_schema(
        parameters=ORDER_LIST_PARAMETERS
    )
    def list(self, request, *args, **kwargs):
        """Get list of orders"""
        return super().list(request, *args, **kwargs)
