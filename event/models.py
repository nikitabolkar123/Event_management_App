from django.db import models
from django.contrib.auth.models import User
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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    #
    # def __str__(self):
    #     return f"Ticket #{self.id} - {self.event.title}"#
# class EventSummary(models.Model):
#     event = models.OneToOneField(Event, on_delete=models.CASCADE)
#     total_tickets_sold = models.PositiveIntegerField(default=0)
#     remaining_seats = models.PositiveIntegerField(default=0)
#
#     def update_summary(self):
#         self.total_tickets_sold = self.event.ticket_set.count()
#         self.remaining_seats = self.event.max_seats - self.total_tickets_sold
#         self.save()
#
#     def __str__(self):
#         return f"Summary for {self.event.title}"
