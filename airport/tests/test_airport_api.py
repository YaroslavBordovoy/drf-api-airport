from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers import AirportSerializer


AIRPORT_URL = reverse("airport:airport-list")


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.airport = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )

    def test_auth_required(self):
        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airports_list(self):
        response = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_airport_retrieve(self):
        url = reverse("airport:airport-detail", args=[self.airport.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.airport.id)

    def test_airport_filter_by_name(self):
        response = self.client.get(AIRPORT_URL, {"closest_big_city": "Atlanta"})
        airports = Airport.objects.filter(closest_big_city="Atlanta")
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class AdminAirportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.admin)

    def test_airport_creation(self):
        data = {
            "name": "Atlanta Airport",
            "closest_big_city": "Atlanta",
        }
        response = self.client.post(AIRPORT_URL, data)
        airport = Airport.objects.get(id=response.data["id"])
        serializer = AirportSerializer(airport)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
