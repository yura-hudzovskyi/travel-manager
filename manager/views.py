from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView

from manager.forms import TicketForm
from manager.models import Hotel, Route, Trip, Ticket


def ajax_load_routes_and_hotels(request):
    trip_id = request.GET.get('trip_id')
    route_id = request.GET.get('route_id')
    data = {}

    if trip_id:
        routes = Route.objects.filter(trip_id=trip_id).order_by('duration')
        hotels = Hotel.objects.filter(trips__id=trip_id).order_by('name')
        data['routes'] = [{'id': route.id, 'name': route.name} for route in routes]
        data['hotels'] = [{'id': hotel.id, 'name': hotel.name} for hotel in hotels]

    if route_id:
        hotels = Hotel.objects.filter(routes__id=route_id).order_by('name')
        data['hotels'] = [{'id': hotel.id, 'name': hotel.name} for hotel in hotels]

    return JsonResponse(data)


@login_required
def index(request: HttpRequest) -> HttpResponse:
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


def create_ticket(request):
    form = TicketForm()
    return render(request, 'manager/ticket_create.html', {'form': form})
