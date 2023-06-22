from .models import Ticket
from .serializers import TicketSerializer
from django.utils import timezone
from datetime import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from event.models import Event
from event.serializers import EventSerializer


class EventAPIViews(APIView):
    serializer_class = EventSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response({'message': 'You do not have permission to create a new event'}, status=403)
        try:
            request.data.update({'user': request.user.id})
            serializer = EventSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'event created successfully', 'data': serializer.data, 'status': 201},
                            status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def get(self, request):
        try:
            event = Event.objects.all()
            serializer = EventSerializer(event, many=True)
            return Response({'message': 'event data retrieved successfully', 'data': serializer.data, 'status': 200},
                            status=200)
        except Exception as e:
            # logger.exception(e)
            return Response({'message': str(e)}, status=400)

    def put(self, request, event_id):
        if not request.user.is_superuser:
            return Response({'message': 'You do not have permission to update book'}, status=403)
        try:
            request.data.update({'user': request.user.id})  #
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "event Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            # logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)

    def delete(self, request, event_id):
        if not request.user.is_superuser:
            return Response({'message': 'You do not have permission to delete event'}, status=403)
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return Response({"message": "event deleted Successfully", "status": 200, "data": {}},
                            status=200)
        except Exception as e:
            # logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)


class TicketAPIViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tickets = Ticket.objects.filter(user=user)
        serializer = TicketSerializer(tickets, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        user = request.user
        event_id = request.data.get('event_id')
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        if event.booking_open_window_start <= timezone.now() <= event.booking_open_window_end:
            existing_tickets = Ticket.objects.filter(user=user, event=event)
            if existing_tickets.count() >= event.max_seats:
                return Response({'message': 'Ticket limit exceeded'}, status=status.HTTP_400_BAD_REQUEST)
            ticket = Ticket(user=user, event=event)
            ticket.save()
            serializer = TicketSerializer(ticket)
            return Response({'message': 'Ticket booked successfully', 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Booking window closed'}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, ticket_id):
    #     # user = request.user
    #     try:
    #         ticket = Ticket.objects.get(id=ticket_id)
    #         ticket.delete()
    #         return Response({'message': 'Ticket deleted successfully'}, status=status.HTTP_200_OK)
    #     except Ticket.DoesNotExist:
    #         return Response({'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(pk=ticket_id, user=request.user)
            ticket.delete()
            return Response({'message': 'Ticket deleted successfully'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
