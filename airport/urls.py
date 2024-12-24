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

router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("routes", RouteViewSet)
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("tickets", TicketViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]
