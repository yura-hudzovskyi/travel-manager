from django import forms

from manager.models import Ticket, Route, Hotel


class DateInput(forms.DateInput):
    input_type = "date"


class TicketForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none())
    date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Ticket
        fields = ('route', 'hotel', 'date')

    def __init__(self, *args, **kwargs):
        trip_pk = kwargs.pop('trip_pk')
        super().__init__(*args, **kwargs)
        self.fields['route'].queryset = Route.objects.filter(trip__pk=trip_pk)
        self.fields['hotel'].queryset = Hotel.objects.filter(trips__pk=trip_pk)
        self.fields['route'].widget.attrs.update({
            'class': 'js-example-basic-single js-states form-control',
            'style': 'width: 100%;'
        })
        self.fields['hotel'].widget.attrs.update({
            'class': 'js-example-basic-single js-states form-control',
            'style': 'width: 100%;'
        })
        self.fields['date'].widget.attrs.update({
            "class": "form-control",
            "id": "pro-bootstrap-date-departure",
            "placeholder": "",
            "type": "text"
        })
