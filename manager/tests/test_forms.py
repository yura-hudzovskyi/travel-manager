import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.forms import TicketForm, UserCreateForm
from manager.models import Hotel, Trip, Route


class TicketFormTest(TestCase):
    def setUp(self) -> None:
        hotel = Hotel.objects.create(name="Hotel", address="Address", description="Description", price=100)
        trip = Trip.objects.create(title="Trip", description="Description", price=100)
        trip.hotel.add(hotel)
        route = Route.objects.create(trip=trip, departure="Departure", arrival="Arrival", duration=datetime.timedelta(days=1))
        user = get_user_model().objects.create_user(username="testuser", password="12345")
        self.client.force_login(user)
        self.client.post(reverse("manager:ticket-create", args=[trip.id]), data={
            "route": route.id,
            "hotel": hotel.id,
            "date": datetime.date.today(),
        })

    def test_that_date_cannot_be_in_the_past(self):
        hotel = Hotel.objects.first()
        trip = Trip.objects.first()
        route = Route.objects.first()
        form = TicketForm(data={
            "route": route.id,
            "hotel": hotel.id,
            "date": datetime.date.today() - datetime.timedelta(days=1),
        }, trip_pk=trip.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["date"], ["Date cannot be in the past!"])

    def test_that_form_is_valid(self):
        hotel = Hotel.objects.first()
        trip = Trip.objects.first()
        route = Route.objects.first()
        form = TicketForm(data={
            "route": route.id,
            "hotel": hotel.id,
            "date": datetime.date.today(),
        }, trip_pk=trip.id)
        self.assertTrue(form.is_valid())


class UserCreateFormTest(TestCase):
    def test_that_form_has_all_fields(self):
        form = UserCreateForm()
        fields = list(form.fields.keys())
        self.assertEqual(sorted(fields), sorted(["username", "password1", "password2", "first_name", "last_name", "email"]))
