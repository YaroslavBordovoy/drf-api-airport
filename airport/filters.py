from django.contrib import admin


class DistanceRangeFilterAdmin(admin.SimpleListFilter):
    title = "Distance Range"
    parameter_name = "distance_range"

    def lookups(self, request, model_admin):
        return [
            ("short", "0-2000 km"),
            ("medium", "2001-5000 km"),
            ("long", ">5001 km"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "short":
            return queryset.filter(distance__lte=2000)
        elif self.value() == "medium":
            return queryset.filter(distance__gt=2000, distance__lte=5000)
        elif self.value() == "long":
            return queryset.filter(distance__gte=5001)

        return queryset
