from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from airport.services.airplane_image import airplane_image_file_path


class Flight(models.Model):
    route = models.ForeignKey(
        to="Route",
        on_delete=models.CASCADE,
        related_name="route_flights"
    )
    airplane = models.ForeignKey(
        to="Airplane",
        on_delete=models.CASCADE,
        related_name="airplane_flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(to="Crew", related_name="crew_flights")

    class Meta:
        ordering = ("route", "departure_time")

    @staticmethod
    def validate_time(
            departure_time,
            arrival_time,
            error_to_raise=ValidationError
    ) -> None:
        if arrival_time < departure_time:
            raise error_to_raise(
                "Arrival time cannot be earlier than departure time."
            )

    def clean(self):
        Flight.validate_time(
            self.departure_time,
            self.arrival_time,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs
    ):
        self.full_clean()
        return super(Flight, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class Crew(models.Model):
    class CrewRole(models.TextChoices):
        PILOT = "P", _("Pilot")
        CO_PILOT = "CP", _("Co-Pilot")
        FLIGHT_ATTENDANT = "FA", _("Flight Attendant")

    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    role = models.CharField(
        max_length=2,
        choices=CrewRole.choices,
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Route(models.Model):
    source = models.ForeignKey(
        to="Airport",
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        to="Airport",
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.PositiveIntegerField(
        help_text="Enter the distance between airports in kilometers."
    )

    def __str__(self) -> str:
        return f"{self.source} → {self.destination}"

    def clean(self):
        if self.source == self.destination:
            raise ValidationError(
                "Departure and arrival points cannot be the same."
            )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs
    ):
        self.full_clean()
        return super(Route, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class Airport(models.Model):
    name = models.CharField(max_length=127)
    closest_big_city = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"{self.name} ({self.closest_big_city})"

    class Meta:
        unique_together = ("name", "closest_big_city")


class Airplane(models.Model):
    name = models.CharField(
        help_text="Enter aircraft model [company-model-identifier], "
                  "for example: Boeing-737-01.",
        max_length=63,
        unique=True
    )
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        to="AirplaneType",
        on_delete=models.CASCADE,
        related_name="airplanes"
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=airplane_image_file_path,
        default="defaults/default_airplane.jpg",
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def type_of_plane(self):
        if self.capacity < 100:
            return "SM"
        elif 100 < self.capacity < 200:
            return "MD"
        else:
            return "LR"

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs
    ):
        airplane_type_name = self.type_of_plane()
        self.airplane_type = AirplaneType.objects.get_or_create(
            name=airplane_type_name
        )
        super(Airplane, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class AirplaneType(models.Model):
    class AirplaneName(models.TextChoices):
        SMALL = "SM", _("Small plane")
        MEDIUM = "MD", _("Medium plane")
        LARGE = "LR", _("Large plane")

    name = models.CharField(
        max_length=2,
        choices=AirplaneName.choices
    )

    def __str__(self) -> str:
        return self.name


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        to=Flight,
        on_delete=models.CASCADE,
        related_name="flight_tickets"
    )
    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="order_tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "flight")

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        if (not 1 <= row <= airplane.rows
                or not 1 <= seat <= airplane.seats_in_row):
            raise error_to_raise(
                f"Specify row value in range [1, {airplane.rows}], "
                f"seat value in range [1, {airplane.seats_in_row}]"
            )

    def clean(self):
        if not self.flight:
            raise ValidationError("Flight must be specified.")

        airplane = self.flight.airplane

        Ticket.validate_ticket(
            self.row,
            self.seat,
            airplane,
            ValidationError,
        )

    def __str__(self) -> str:
        return (
            f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEl,
        on_delete=models.CASCADE,
        related_name="orders"
    )
