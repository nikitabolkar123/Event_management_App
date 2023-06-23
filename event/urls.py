from django.urls import path

from . import views

urlpatterns = [
    path('admin_event/', views.AdminEventCreateAPIView.as_view(), name='add_event'),
    path('admin_event_list/', views.AdminEventListAPIView.as_view(), name='event'),
    path('admin_update_event/<int:event_id>/', views.AdminEventUpdateAPIView.as_view(), name='event'),
    path('summary_of_event/<int:event_id>/', views.AdminEventSummaryAPIView.as_view(), name='event'),
    path('user_event/', views. UserEventListAPIView.as_view(), name='retrieve_event'),
    path('ticket_event/', views.UserTicketAPIView.as_view(), name='event'),
    path('event1/<int:event_id>/', views.UserEventDetailAPIView.as_view(), name='event'),
    path('book_event/<int:event_id>/', views.UserEventBookingAPIView.as_view(), name='event'),
    path('user_ticket/<int:ticket_id>/', views.UserTicketAPIView.as_view(), name='event'),
]
