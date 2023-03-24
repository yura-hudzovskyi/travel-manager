from django.urls import path

from .views import (
    index,
    HotelListView,
    RouteListView,
    TripListView,
    TicketListView,
    HotelDetailView,
    RouteDetailView,
    TripDetailView,
    TicketDetailView,
    create_ticket as ticket_create_view, ajax_load_routes_and_hotels,
)

urlpatterns = [
    path("", index, name="index"),
    path("hotels/", HotelListView.as_view(), name="hotel-list"),
    path("routes/", RouteListView.as_view(), name="route-list"),
    path("trips/", TripListView.as_view(), name="trip-list"),
    path("tickets/", TicketListView.as_view(), name="ticket-list"),
    path("hotels/<int:pk>/", HotelDetailView.as_view(), name="hotel-detail"),
    path("routes/<int:pk>/", RouteDetailView.as_view(), name="route-detail"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("tickets/create/", ticket_create_view, name="ticket-create"),
    path("tickets/create/ajax", ajax_load_routes_and_hotels, name="ajax_load_routes_and_hotels"),
]

app_name = "manager"
