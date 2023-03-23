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
]

app_name = "manager"
