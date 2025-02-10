from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import AirplaneType, Airplane
from airport.serializers import AirplaneSerializer


AIRPLANE_URL = reverse("airport:airplane-list")


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.airplane_type = AirplaneType.objects.create(name="SM")
        self.airplane_1 = Airplane.objects.create(
            name="B737",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.airplane = Airplane.objects.create(
            name="E190",
            rows=50,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_airplanes_list(self):
        response = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.all()
        serializer = AirplaneSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_airplane_retrieve(self):
        url = reverse("airport:airplane-detail", args=[self.airplane.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.airplane.id)

    def test_airplane_filter_by_name(self):
        response = self.client.get(AIRPLANE_URL, {"name": "B737"})
        airplanes = Airplane.objects.filter(name__icontains="B737")
        serializer = AirplaneSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_airplane_filter_by_airplane_type(self):
        response = self.client.get(AIRPLANE_URL, {"airplane_type": "SM"})
        airplanes = Airplane.objects.filter(airplane_type__name__icontains="SM")
        serializer = AirplaneSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class AdminAirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.admin)
        self.airplane_type = AirplaneType.objects.create(name="SM")

    def test_airplane_creation(self):
        data = {
            "name": "B737",
            "rows": 20,
            "seats_in_row": 6,
            "airplane_type": self.airplane_type.id,
        }
        response = self.client.post(AIRPLANE_URL, data)
        airplane = Airplane.objects.get(id=response.data["id"])
        serializer = AirplaneSerializer(airplane)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
