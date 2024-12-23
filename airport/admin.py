from django.contrib import admin

from airport.models import (
    Flight,
    Crew,
    Route,
    Airport,
    Airplane,
    AirplaneType,
    Ticket,
    Order
)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "airplane_type",
        "rows",
        "seats_in_row",
        "capacity"
    )
    readonly_fields = ("airplane_type",)
    search_fields = ("name",)
    list_filter = ("name", "airplane_type")
    list_per_page = 10


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "closest_big_city")
    search_fields = ("name",)
    list_filter = ("closest_big_city",)
    list_per_page = 10


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    search_fields = ("source",)
    list_filter = ("source",)
    list_per_page = 10


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role")
    search_fields = ("first_name", "last_name")
    list_filter = ("role",)
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user",)
    list_filter = ("created_at",)
    list_per_page = 10


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("order", "flight", "row", "seat")
    search_fields = ("order__user__username",)
    list_filter = ("flight",)
    list_per_page = 10


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("route", "airplane", "departure_time", "arrival_time")
    search_fields = ("route",)
    list_filter = ("route",)
    list_per_page = 10


admin.site.register(AirplaneType)
