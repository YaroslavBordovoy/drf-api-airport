from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
    Crew,
)
from airport.serializers import (
    FlightListSerializer,
    FlightDetailSerializer, FlightSerializer
)


FLIGHT_URL = reverse("airport:flight-list")


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTests(TestCase):
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
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="SM")
        self.airplane = Airplane.objects.create(
            name="B737",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.crew_1 = Crew.objects.create(
            first_name="test_pilot",
            last_name="test_pilot_last_name",
            role="P"
        )
        self.crew_2 = Crew.objects.create(
            first_name="test_co_pilot",
            last_name="test_co_pilot_last_name",
            role="CP"
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2025-01-02 15:00:00",
            arrival_time="2025-01-03 15:00:00"
        )
        self.flight.crew.add(self.crew_1, self.crew_2)

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_flights_list(self):
        response = self.client.get(FLIGHT_URL)
        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            self.assertIn("tickets_available", flight)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flight_retrieve(self):
        url = reverse("airport:flight-detail", args=[self.flight.id])
        serializer = FlightDetailSerializer(self.flight)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_flights_filter_by_airplane_name(self):
        response = self.client.get(
            FLIGHT_URL,
            {
                "airplane_name": "B737",
            }
        )
        flights = Flight.objects.filter(
            airplane__name="B737"
        )
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flights_filter_by_departure_airport(self):
        response = self.client.get(
            FLIGHT_URL,
            {
                "departure_airport": "Atlanta",
            }
        )
        flights = Flight.objects.filter(
            route__source__closest_big_city="Atlanta"
        )
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flights_filter_by_arrival_airport(self):
        response = self.client.get(
            FLIGHT_URL,
            {
                "arrival_airport": "New York",
            }
        )
        flights = Flight.objects.filter(
            route__destination__closest_big_city="New York"
        )
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flights_filter_by_departure_time(self):
        today = now().date()

        response = self.client.get(
            FLIGHT_URL,
            {
                "departure_time": today.isoformat(),
            }
        )
        flights = Flight.objects.filter(
            departure_time=today
        )
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flights_filter_by_arrival_time(self):
        today = now().date()

        response = self.client.get(
            FLIGHT_URL,
            {
                "arrival_airport": today.isoformat(),
            }
        )
        flights = Flight.objects.filter(
            arrival_time=today
        )
        serializer = FlightListSerializer(flights, many=True)

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class AdminFlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.admin)
        self.source_airport = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )
        self.destination_airport = Airport.objects.create(
            name="New York Airport",
            closest_big_city="New York"
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="SM")
        self.airplane = Airplane.objects.create(
            name="B737",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.crew_1 = Crew.objects.create(
            first_name="test_pilot",
            last_name="test_pilot_last_name",
            role="P"
        )
        self.crew_2 = Crew.objects.create(
            first_name="test_co_pilot",
            last_name="test_co_pilot_last_name",
            role="CP"
        )

    def test_flight_creation(self):
        data = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": "2025-01-02 15:00:00",
            "arrival_time": "2025-01-03 15:00:00",
            "crew": [self.crew_1.id, self.crew_2.id]
        }
        response = self.client.post(FLIGHT_URL, data)

        flight = Flight.objects.get(id=response.data["id"])
        serializer = FlightSerializer(flight)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
