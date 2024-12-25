from django.urls import path, include
from rest_framework import routers

from airport.views import (
    FlightViewSet,
    CrewViewSet,
    RouteViewSet,
    AirportViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    TicketViewSet,
    OrderViewSet
)


app_name = "airport"

router = routers.DefaultRouter()

router.register("flights", FlightViewSet, basename="flight")
router.register("crews", CrewViewSet)
router.register("routes", RouteViewSet, basename="route")
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet, basename="airplane")
router.register("airplane-types", AirplaneTypeViewSet)
router.register("tickets", TicketViewSet, basename="ticket")
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]
