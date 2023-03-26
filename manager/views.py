from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from manager.forms import TicketForm
from manager.models import Hotel, Route, Trip, Ticket


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
    paginate_by = 6


class TripListView(LoginRequiredMixin, generic.ListView):
    model = Trip
    paginate_by = 6


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


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


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "manager/create_ticket.html"
    success_url = reverse_lazy("manager:ticket-detail")

    def form_valid(self, form):
        # Set the current user as the ticket's user
        form.instance.user = self.request.user

        # Set the ticket's route based on the selected trip
        trip_pk = self.kwargs["trip_pk"]
        trip = get_object_or_404(Trip, pk=trip_pk)
        form.instance.route = trip.routes.first()

        # calculate the ticket's price
        hotel_price = form.cleaned_data["hotel"].price
        trip_price = trip.price
        form.instance.price = hotel_price + trip_price
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["trip_pk"] = self.kwargs["trip_pk"]
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_pk = self.kwargs["trip_pk"]
        trip = get_object_or_404(Trip, pk=trip_pk)
        context["trip"] = trip
        context["routes"] = trip.routes.all()
        context["hotels"] = Hotel.objects.filter(trips=trip)
        return context

    def get_success_url(self):
        return reverse_lazy("manager:ticket-detail", kwargs={"pk": self.object.pk})


