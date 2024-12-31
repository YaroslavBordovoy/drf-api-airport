from django.contrib.auth import get_user_model
from django.test import TestCase
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
    Ticket,
    Order
)
from airport.serializers import (
    TicketListSerializer,
    TicketDetailSerializer,
    TicketSerializer
)


TICKET_URL = reverse("airport:ticket-list")


class UnauthenticatedTicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TICKET_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.source_airport_1 = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )
        self.destination_airport_1 = Airport.objects.create(
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
            source=self.source_airport_1,
            destination=self.destination_airport_1,
            distance=1000
        )
        self.route_2 = Route.objects.create(
            source=self.source_airport_2,
            destination=self.destination_airport_2,
            distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="SM")
        self.airplane_1 = Airplane.objects.create(
            name="B737",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.airplane_2 = Airplane.objects.create(
            name="E190",
            rows=50,
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
            airplane=self.airplane_1,
            departure_time="2025-01-02 15:00:00",
            arrival_time = "2025-01-03 15:00:00"
        )
        self.flight.crew.add(self.crew_1, self.crew_2)
        self.order = Order.objects.create(
            user=self.user
        )
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            order=self.order,
            flight=self.flight
        )

    def test_auth_required(self):
        response = self.client.get(TICKET_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tickets_list(self):
        response = self.client.get(TICKET_URL)
        tickets = Ticket.objects.all()
        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_ticket_retrieve(self):
        url = reverse("airport:ticket-detail", args=[self.ticket.id])
        serializer = TicketDetailSerializer(self.ticket)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tickets_filter_by_source_city(self):
        response = self.client.get(
            TICKET_URL,
            {
                "flight_from": "Dnipro",
            }
        )
        tickets = Ticket.objects.filter(
            flight__route__source__closest_big_city__icontains="Dnipro"
        )
        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_tickets_filter_by_destination_city(self):
        response = self.client.get(
            TICKET_URL,
            {
                "flight_to": "Kyiv",
            }
        )
        tickets = Ticket.objects.filter(
            flight__route__destination__closest_big_city__icontains="Kyiv"
        )
        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class AdminTicketTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.admin)
        self.source_airport_1 = Airport.objects.create(
            name="Atlanta Airport",
            closest_big_city="Atlanta"
        )
        self.destination_airport_1 = Airport.objects.create(
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
            source=self.source_airport_1,
            destination=self.destination_airport_1,
            distance=1000
        )
        self.route_2 = Route.objects.create(
            source=self.source_airport_2,
            destination=self.destination_airport_2,
            distance=1000
        )
        self.airplane_type = AirplaneType.objects.create(name="SM")
        self.airplane_1 = Airplane.objects.create(
            name="B737",
            rows=20,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.airplane_2 = Airplane.objects.create(
            name="E190",
            rows=50,
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
            airplane=self.airplane_1,
            departure_time="2025-01-02 15:00:00",
            arrival_time="2025-01-03 15:00:00"
        )
        self.flight.crew.add(self.crew_1, self.crew_2)
        self.order = Order.objects.create(
            user=self.admin
        )

    def test_route_creation(self):
        data = {
            "seat": 1,
            "row": 5,
            "order": self.admin.id,
            "flight": self.flight.id
        }
        response = self.client.post(TICKET_URL, data)
        ticket = Ticket.objects.get(id=response.data["id"])
        serializer = TicketSerializer(ticket)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
