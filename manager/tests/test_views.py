from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import datetime

from manager.models import Trip, Hotel, Route, Ticket


class TicketCreateViewTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.client.force_login(user)

    def test_that_route_and_hotels_displayed_depend_on_trip(self) -> None:
        hotel1 = Hotel.objects.create(
            name="Hotel1",
            address="Address1",
            description="Description1",
            price=100,
        )
        hotel2 = Hotel.objects.create(
            name="Hotel2",
            address="Address2",
            description="Description2",
            price=200,
        )
        trip = Trip.objects.create(
            title="Trip1",
            description="Description1",
            price=100,
        )
        trip.hotel.set([hotel1, hotel2])
        route1 = Route.objects.create(
            departure="Departure1",
            arrival="Arrival1",
            duration=datetime.timedelta(hours=1),
            trip=trip,
        )

        response = self.client.get(reverse("manager:ticket-create", args=[trip.id]))
        self.assertContains(response, hotel1.name)
        self.assertContains(response, hotel2.name)
        self.assertContains(response, route1)

    def test_that_ticket_created_with_full_price(self) -> None:
        hotel1 = Hotel.objects.create(
            name="Hotel1",
            address="Address1",
            description="Description1",
            price=100,
        )
        trip = Trip.objects.create(
            title="Trip1",
            description="Description1",
            price=100,
        )
        trip.hotel.set([hotel1])
        route1 = Route.objects.create(
            departure="Departure1",
            arrival="Arrival1",
            duration=datetime.timedelta(hours=1),
            trip=trip,
        )

        response = self.client.post(
            reverse("manager:ticket-create", args=[trip.id]),
            data={
                "hotel": hotel1.id,
                "route": route1.id,
                "date": datetime.date.today(),
            },
        )

        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.first().price, 200)

    def test_redirect_to_ticket_detail_page_after_creation(self) -> None:
        hotel1 = Hotel.objects.create(
            name="Hotel1",
            address="Address1",
            description="Description1",
            price=100,
        )
        trip = Trip.objects.create(
            title="Trip1",
            description="Description1",
            price=100,
        )
        trip.hotel.set([hotel1])
        route1 = Route.objects.create(
            departure="Departure1",
            arrival="Arrival1",
            duration=datetime.timedelta(hours=1),
            trip=trip,
        )

        response = self.client.post(
            reverse("manager:ticket-create", args=[trip.id]),
            data={
                "hotel": hotel1.id,
                "route": route1.id,
                "date": datetime.date.today(),
            },
        )

        self.assertRedirects(
            response,
            reverse("manager:ticket-detail", args=[Ticket.objects.first().number]),
        )


class UserUpdateView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            password="12345",
            first_name="Test",
            last_name="User",
            email="user@user.com",
        )
        self.client.force_login(user)

    def test_that_user_data_displayed_in_form(self) -> None:
        response = self.client.get(
            reverse("manager:profile", args=[User.objects.first().id])
        )

        self.assertContains(response, "Test")
        self.assertContains(response, "User")
        self.assertContains(response, "testuser")
        self.assertContains(response, "user@user.com")

    def test_that_user_data_updated(self) -> None:
        response = self.client.post(
            reverse("manager:profile", args=[User.objects.first().id]),
            data={
                "first_name": "Test1",
                "last_name": "User1",
                "username": "testuser1",
                "email": "admin@admin.com",
            },
        )

        self.assertRedirects(
            response,
            reverse("manager:profile", args=[User.objects.first().id])
            + "?success=True",
        )
        self.assertEqual(User.objects.first().first_name, "Test1")
        self.assertEqual(User.objects.first().last_name, "User1")
        self.assertEqual(User.objects.first().username, "testuser1")
        self.assertEqual(User.objects.first().email, "admin@admin.com")

    def test_that_success_message_displayed(self) -> None:
        redirect_url = (
            reverse("manager:profile", args=[User.objects.first().id]) + "?success=True"
        )
        response = self.client.get(redirect_url)
        self.assertContains(response, "Profile updated successfully")

    def test_that_error_message_displayed(self) -> None:
        response = self.client.post(
            reverse("manager:profile", args=[User.objects.first().id]),
            data={
                "first_name": "Test1",
                "last_name": "User1",
                "username": "testuser1",
                "email": "dsdsad",
            },
        )

        self.assertContains(response, "Enter a valid email address.")


class PasswordChangeView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            password="12345",
        )
        self.client.force_login(user)

    def test_that_password_changed(self) -> None:
        response = self.client.post(
            reverse("manager:password-change"),
            data={
                "new_password1": "1qazcdvfr4",
                "new_password2": "1qazcdvfr4",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.first().check_password("1qazcdvfr4"))

    def test_that_error_message_displayed(self) -> None:
        response = self.client.post(
            reverse("manager:password-change"),
            data={
                "new_password1": "1qazcdvfr4",
                "new_password2": "1qazcdvfr",
            },
        )
        self.assertContains(response, "The two password fields didn’t match.")
