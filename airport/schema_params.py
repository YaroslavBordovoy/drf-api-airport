from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


FLIGHT_LIST_PARAMETERS = [
    OpenApiParameter(
        name="airplane_name",
        description="Filter by airplane name",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="departure_airport",
        description="Filter by closest big city of departure airport",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="arrival_airport",
        description="Filter by closest big city of arrival airport",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="departure_time",
        description="Filter by departure time (YYYY-MM-DD)",
        required=False,
        type=OpenApiTypes.DATE,
    ),
    OpenApiParameter(
        name="arrival_time",
        description="Filter by arrival time (YYYY-MM-DD)",
        required=False,
        type=OpenApiTypes.STR,
    ),
]

CREW_LIST_PARAMETERS = [
    OpenApiParameter(
        name="role",
        description="Filter by role (P, CP, FA)",
        required=False,
        type=OpenApiTypes.STR,
    )
]

ROUTE_LIST_PARAMETERS = [
    OpenApiParameter(
        name="source_city",
        description="Filter by closest big city of departure airport",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="destination_city",
        description="Filter by closest big city of arrival airport",
        required=False,
        type=OpenApiTypes.STR,
    )
]

AIRPORT_LIST_PARAMETERS = [
    OpenApiParameter(
        name="name",
        description="Filter by closest big city",
        required=False,
        type=OpenApiTypes.STR,
    )
]

AIRPLANE_LIST_PARAMETERS = [
    OpenApiParameter(
        name="name",
        description="filter by airplane (B737, E190)",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="airplane_type",
        description="filter by airplane type (SM, MD, LR)",
        required=False,
        type=OpenApiTypes.STR,
    )
]

TICKET_LIST_PARAMETERS = [
    OpenApiParameter(
        name="flight_from",
        description="Filter by closest big city of departure airport",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="flight_to",
        description="Filter by closest big city of arrival airport",
        required=False,
        type=OpenApiTypes.STR,
    )
]

ORDER_LIST_PARAMETERS = [
    OpenApiParameter(
        name="created_at",
        description="Filter by creation time (YYYY-MM-DD)",
        required=False,
        type=OpenApiTypes.STR,
    )
]
