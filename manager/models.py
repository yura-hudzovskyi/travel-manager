import secrets

from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    hotel = models.ManyToManyField(Hotel, related_name="trips")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Route(models.Model):
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    duration = models.DurationField()
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="routes")

    class Meta:
        ordering = ["duration"]

    def __str__(self):
        return f"{self.departure} - {self.arrival}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="tickets")
    date = models.DateField()
    number = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = int("1" + str(secrets.randbits(15)))
            while Ticket.objects.filter(number=self.number).exists():
                self.number = int("1" + str(secrets.randbits(15)))
        super().save(*args, **kwargs)
        return self
