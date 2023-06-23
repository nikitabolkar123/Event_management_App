from rest_framework.permissions import IsAuthenticated
from event.models import Event, Ticket
from event.serializers import EventSerializer, TicketSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from logconfig.logger import get_logger
from .models import Event
from .serializers import EventSerializer
# Logger configuration
logger = get_logger()


class UserEventListAPIView(APIView):
    serializer_class = EventSerializer
    """
          class is used for the user event list data
       """

    def get(self, request):
        try:
            events = Event.objects.all().order_by('start_date')
            serializer = EventSerializer(events, many=True)
            return Response({'message': 'Event data retrieved successfully', 'data': serializer.data, 'status': 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserEventDetailAPIView(APIView):
    serializer_class = EventSerializer
    """
          class is used for the user event details
       """

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


class UserEventBookingAPIView(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    """
          class is used for the user 
       """

    def post(self, request, event_id):
        """
        POST API for booking an event
        """
        user = request.user
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if event.event_type == 'online':
            if not event.is_booking_open():
                return Response({'message': 'Booking window closed'}, status=status.HTTP_400_BAD_REQUEST)

        if event.get_remaining_seats() <= 0:
            return Response({'message': 'Ticket limit exceeded'}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.create(event=event, user=user)
        serializer = self.serializer_class(ticket)
        return Response({'message': 'Ticket booked successfully', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)


class UserTicketAPIView(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    """
          class is used for the user ticket
       """

    def get(self, request):
        try:
            user = request.user
            tickets = Ticket.objects.filter(user=user)
            serializer = self.serializer_class(tickets, many=True)
            return Response({'message': 'Tickets retrieved successfully', 'data': serializer.data, 'status': 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminEventCreateAPIView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    """
          class is used for the Admin crud
       """

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
            logger.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminEventListAPIView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    """
          class is used for the admin to retrieve event list
       """

    def get(self, request):
        try:
            events = Event.objects.all()
            serializer = self.serializer_class(events, many=True)
            return Response({'message': 'Event data retrieved successfully', 'data': serializer.data, 'status': 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminEventUpdateAPIView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    """
          class is used for the Admin to update event data
       """
    def put(self, request, event_id):
        try:
            request.data.update({'user': request.user.id})  #
            event = Event.objects.get(id=event_id)
            serializer = EventSerializer(event, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "event Updated Successfully", "status": 200, "data": serializer.data},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400, "data": {}}, status=400)


class AdminEventSummaryAPIView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]
    """
          class is used for the Admin to show summary od event
       """

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'message': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        summary = event.get_event_summary()
        return Response({
            'message': 'Event summary retrieved successfully',
            'data': summary,
            'status': status.HTTP_200_OK
        })
