from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import Crew
from airport.serializers import CrewSerializer

CREW_URL = reverse("airport:crew-list")


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
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
        self.crew_3 = Crew.objects.create(
            first_name="test_fa",
            last_name="test_fa_last_name",
            role="FA"
        )

    def test_auth_required(self):
        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crews_list(self):
        response = self.client.get(CREW_URL)
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(len(response.data["results"]), 3)

    def test_crew_retrieve(self):
        url = reverse("airport:crew-detail", args=[self.crew_1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.crew_1.id)

    def test_crews_filter_by_role(self):
        response = self.client.get(CREW_URL, {"role": "FA"})
        crews = Crew.objects.filter(role__icontains="FA")
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(len(response.data["results"]), 1)


class AdminCrewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.admin)

    def test_crew_creation(self):
        data = {
            "first_name": "test_name",
            "last_name": "test_last_name",
            "role": "PILOT"
        }

        response = self.client.post(CREW_URL, data)

        crew = Crew.objects.get(id=response.data["id"])
        serializer = CrewSerializer(crew)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
