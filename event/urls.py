from django.urls import path

from . import views

urlpatterns = [
    path('event/', views.EventAPIViews.as_view(), name='eventt'),
    path('event/<int:event_id>/', views.EventAPIViews.as_view(), name='eventt'),
    path('ticket/', views.TicketAPIViews.as_view(), name='event'),
    path('ticket/<int:ticket_id>/', views.TicketAPIViews.as_view(), name='event'),

]
