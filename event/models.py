from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from user.models import User


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_seats = models.PositiveIntegerField()
    booking_open_window_start = models.DateTimeField()
    booking_open_window_end = models.DateTimeField()

    def is_booking_open(self):
        now = timezone.now()
        return self.booking_open_window_start <= now <= self.booking_open_window_end

    def get_total_tickets_sold(self):
        return self.tickets.count()

    def get_remaining_seats(self):
        return self.max_seats - self.get_total_tickets_sold()

    def get_event_summary(self):
        return {
            'total_tickets_sold': self.get_total_tickets_sold(),
            'remaining_seats': self.get_remaining_seats()
        }


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

