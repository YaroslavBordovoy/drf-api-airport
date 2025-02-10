from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Airport, Route
from airport.serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)


ROUTE_URL = reverse("airport:route-list")


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.source_airport = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )
        self.destination_airport = Airport.objects.create(
            name="New York Airport",
            closest_big_city="New York"
        )
        self.source_airport_2 = Airport.objects.create(
            name="Kyiv Airport",
            closest_big_city="Kyiv"
        )
        self.destination_airport_2 = Airport.objects.create(
            name="Dnipro Airport",
            closest_big_city="Dnipro"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=1000
        )
        self.route_2 = Route.objects.create(
            source=self.source_airport_2,
            destination=self.destination_airport_2,
            distance=1000
        )

    def test_auth_required(self):
        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routes_list(self):
        response = self.client.get(ROUTE_URL)
        routes = Route.objects.all()
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_route_retrieve(self):
        url = reverse("airport:route-detail", args=[self.route.id])
        serializer = RouteDetailSerializer(self.route)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_routes_filter_by_source_city(self):
        response = self.client.get(
            ROUTE_URL,
            {
                "source_city": "Atlanta",
            }
        )
        routes = Route.objects.filter(
            source__closest_big_city__icontains="Atlanta"
        )
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_routes_filter_by_destination_city(self):
        response = self.client.get(
            ROUTE_URL,
            {
                "destination_city": "Dnipro",
            }
        )
        routes = Route.objects.filter(
            destination__closest_big_city__icontains="Dnipro"
        )
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)



class AdminRouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.admin)
        self.source_airport = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )
        self.destination_airport = Airport.objects.create(
            name="New York Airport",
            closest_big_city="New York"
        )

    def test_route_creation(self):
        data = {
            "source": self.source_airport.id,
            "destination": self.destination_airport.id,
            "distance": 1000,
        }
        response = self.client.post(ROUTE_URL, data)
        route = Route.objects.get(id=response.data["id"])
        serializer = RouteSerializer(route)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
