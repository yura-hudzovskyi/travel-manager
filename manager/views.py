from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from manager.models import Hotel, Route, Trip, Ticket


@login_required
def index(request: HttpResponse) -> HttpResponse:
    return render(request, "manager/index.html")


class HotelListView(LoginRequiredMixin, generic.ListView):
    model = Hotel
    template_name = "manager/hotel_list.html"
    context_object_name = "hotels"
    paginate_by = 5


class RouteListView(LoginRequiredMixin, generic.ListView):
    model = Route
    template_name = "manager/route_list.html"
    context_object_name = "routes"
    paginate_by = 5


class TripListView(LoginRequiredMixin, generic.ListView):
    model = Trip
    paginate_by = 5


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    paginate_by = 5


class HotelDetailView(LoginRequiredMixin, generic.DetailView):
    model = Hotel
    template_name = "manager/hotel_detail.html"


class RouteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Route
    template_name = "manager/route_detail.html"


class TripDetailView(LoginRequiredMixin, generic.DetailView):
    model = Trip


class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket

