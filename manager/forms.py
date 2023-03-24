from django import forms
from .models import Trip, Route, Ticket, Hotel


class TicketForm(forms.ModelForm):
    trip = forms.ModelChoiceField(queryset=Trip.objects.all())
    route = forms.ModelChoiceField(queryset=Route.objects.none())
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none())

    class Meta:
        model = Ticket
        fields = ("trip", "route", "hotel", "date", "number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["route"].queryset = Route.objects.none()
        self.fields["hotel"].queryset = Hotel.objects.none()

        if "trip" in self.data:
            try:
                trip_id = int(self.data.get("trip"))
                self.fields["route"].queryset = Route.objects.filter(trip_id=trip_id).order_by("duration")
                self.fields["hotel"].queryset = Hotel.objects.filter(trips__id=trip_id).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["route"].queryset = self.instance.trip.routes.order_by("duration")
            self.fields["hotel"].queryset = self.instance.trip.hotel_set.order_by("name")
