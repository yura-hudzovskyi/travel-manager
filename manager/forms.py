import datetime
from django.contrib.auth.forms import SetPasswordForm

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from manager.models import Ticket, Route, Hotel


class DateInput(forms.DateInput):
    input_type = "date"


class TicketForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none())
    date = forms.DateField(widget=DateInput(attrs={"type": "date"}))

    class Meta:
        model = Ticket
        fields = ("route", "hotel", "date")

    def __init__(self, *args, **kwargs):
        trip_pk = kwargs.pop("trip_pk")
        super().__init__(*args, **kwargs)
        self.fields["route"].queryset = Route.objects.filter(trip__pk=trip_pk)
        self.fields["hotel"].queryset = Hotel.objects.filter(trips__pk=trip_pk)
        self.fields["route"].widget.attrs.update(
            {
                "class": "js-example-basic-single js-states form-control",
                "style": "width: 100%;",
            }
        )
        self.fields["hotel"].widget.attrs.update(
            {
                "class": "js-example-basic-single js-states form-control",
                "style": "width: 100%;",
            }
        )
        self.fields["date"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "pro-bootstrap-date-departure",
                "placeholder": "",
                "type": "text",
            }
        )

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < datetime.date.today():
            raise forms.ValidationError("Date cannot be in the past!")
        return date


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm Password"}
        )
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "First Name",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Last Name"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        print(self.fields["username"].error_messages)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "First Name",
                "value": user.first_name,
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Last Name",
                "value": user.last_name,
            }
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Email",
                "value": user.email,
            }
        )
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Username",
                "value": user.username,
            }
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            User.objects.filter(email=email)
            .exclude(username=self.instance.username)
            .exists()
        ):
            raise forms.ValidationError("Email already exists!")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (
            User.objects.filter(username=username)
            .exclude(username=self.instance.username)
            .exists()
        ):
            raise forms.ValidationError("Username already exists!")
        return username


class SetPasswordForm1(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm Password"}
        )
