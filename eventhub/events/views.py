

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Reservation
from .serializers import EventSerializer, ReservationSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        status_param = self.request.query_params.get('status')
        venue_param = self.request.query_params.get('venue')

        if status_param:
            queryset = queryset.filter(status=status_param)

        if venue_param:
            queryset = queryset.filter(venue__icontains=venue_param)

        return queryset
         
    serializer_class = EventSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    
    serializer_class = ReservationSerializer

    def get_queryset(self):
        
        queryset = Reservation.objects.all()

        event_id = self.request.query_params.get('event_id')

        if event_id:
            queryset = queryset.filter(event__id=event_id)

        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()

        if reservation.status == 'cancelled':
            return Response({'detail': 'Reservation is already cancelled.'}, status=400)

        reservation.status = 'cancelled'
        reservation.save()

        # Update the available seats for the event
        event = reservation.event
        event.available_seats += reservation.seats_reserved
        event.save()

        return Response(self.get_serializer(reservation).data)
