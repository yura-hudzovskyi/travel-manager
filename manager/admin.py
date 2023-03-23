from django.contrib import admin

from manager.models import Trip, Hotel, Route, Ticket


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "hotel"]
    list_filter = ["hotel"]
    search_fields = ["title", "hotel__name"]
    ordering = ["title"]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "price"]
    search_fields = ["name", "address"]
    ordering = ["name"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["departure", "arrival", "duration", "trip"]
    list_filter = ["trip"]
    search_fields = ["departure", "arrival", "trip__title"]
    ordering = ["duration"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["user", "price", "route", "date", "number"]
    list_filter = ["route__trip", "date"]
    search_fields = ["user__username", "route__trip__title"]
    ordering = ["date"]
