from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from airport.services.utils.airplane_image import airplane_image_file_path
from airport.choices import (
    AirplaneName,
    AirplaneTypeName,
    CrewRole
)
from airport.services.utils.distance_calcultion import (
    get_coord,
    calculate_distance
)
from airport.services.utils.city_verification import get_city


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

    def __str__(self) -> str:
        return str(self.route)

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
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    role = models.CharField(
        max_length=3,
        choices=CrewRole.choices,
    )

    class Meta:
        ordering = ("role",)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.role})"


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

    @property
    def route(self):
        return self.__str__()

    def clean(self):
        if self.source == self.destination:
            raise ValidationError(
                "Departure and arrival points cannot be the same."
            )

        try:
            self.distance = calculate_distance(
                source_coords=get_coord(self.source.closest_big_city),
                destination_coords=get_coord(self.destination.closest_big_city)
            )
        except ValidationError as e:
            raise ValidationError(f"Error calculating distance: {e}")

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
        ordering = ("name",)
        unique_together = ("name", "closest_big_city")

    def clean(self):
        is_existing_city = get_city(self.closest_big_city)

        if not is_existing_city:
            raise ValidationError("The entered city does not exist.")

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs
    ):
        self.full_clean()
        return super(Airport, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class Airplane(models.Model):
    name = models.CharField(
        max_length=7,
        choices=AirplaneName.choices
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

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.get_name_display()

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
        self.airplane_type, _ = AirplaneType.objects.get_or_create(
            name=airplane_type_name
        )
        super(Airplane, self).save(
            force_insert, force_update, using, update_fields, **kwargs
        )


class AirplaneType(models.Model):
    name = models.CharField(
        max_length=3,
        choices=AirplaneTypeName.choices
    )

    def __str__(self) -> str:
        return f"{self.get_name_display()} ({self.name})"


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
        related_name="order_tickets",
        null=True,
        blank=True
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
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self) -> str:
        return (
            f"{self.user} "
            f"(create at: {self.created_at.strftime('%d-%m-%Y %H:%M')})"
        )
