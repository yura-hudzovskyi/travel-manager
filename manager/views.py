from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView


from manager.forms import (
    TicketForm,
    UserCreateForm,
    UserUpdateForm,
    PasswordChangeForm,
    TripSearchForm,
    HotelSearchForm,
    RoutesSearchForm,
)
from manager.models import Hotel, Route, Trip, Ticket


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "manager/index.html")


class HotelListView(LoginRequiredMixin, generic.ListView):
    model = Hotel
    template_name = "manager/hotel_list.html"
    context_object_name = "hotels"
    paginate_by = 6
    queryset = Hotel.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HotelListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search"] = HotelSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = HotelSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])

        return self.queryset.all()


class RouteListView(LoginRequiredMixin, generic.ListView):
    model = Route
    template_name = "manager/route_list.html"
    context_object_name = "routes"
    paginate_by = 6
    queryset = Route.objects.select_related("trip")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RouteListView, self).get_context_data(**kwargs)

        arrival = self.request.GET.get("arrival", "")
        departure = self.request.GET.get("departure", "")

        context["search"] = RoutesSearchForm(
            initial={"arrival": arrival, "departure": departure}
        )

        return context

    def get_queryset(self):
        form = RoutesSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                arrival__icontains=form.cleaned_data["arrival"],
                departure__icontains=form.cleaned_data["departure"],
            )

        return self.queryset.all()


class TripListView(LoginRequiredMixin, generic.ListView):
    model = Trip
    paginate_by = 6
    queryset = Trip.objects.prefetch_related("hotel")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TripListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search"] = TripSearchForm(initial={"title": title})

        return context

    def get_queryset(self):
        form = TripSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(title__icontains=form.cleaned_data["title"])

        return self.queryset.all()


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
    template_name = "manager/ticket_create.html"
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


class UserCreateView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("manager:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("manager:index")


class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ticket
    success_url = reverse_lazy("manager:ticket-list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("manager:profile", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    # add success message to context if form is valid
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET" and self.request.GET.get("success") == "True":
            if self.object:
                messages.success(self.request, "Profile updated successfully")
                context["messages"] = messages.get_messages(self.request)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        response["Location"] += "?success=True"
        return response


@login_required
def password_change(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = PasswordChangeForm(user, request.POST)

    return render(request, "registration/password_change.html", {"form": form})
