from rest_framework import serializers
from .models import Event, Reservation

class EventSerializer(serializers.ModelSerializer):

    reservation_count =serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'venue', 'date', 'total_seats', 'available_seats', 'status', 'created_at', 'reservation_count']

    def get_reservation_count(self, obj):
        return obj.reservations.filter(status='confirmed').count()  

    def validate(self, data):
        if data.get('available_seats') > data.get('total_seats'):
            raise serializers.ValidationError("Available seats cannot exceed total seats.")
        return data  


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'event', 'attendee_name', 'attendee_email', 'seats_reserved', 'status', 'created_at','reservations_count']

        read_only_fields = ['status', 'created_at']

    def validate_seats_reserved(self, value):
        if value <1:
            raise serializers.ValidationError("Seats reserved must be at least 1.")
        return value    

    def validate(self, data):
        event = data.get('event')

        if event.status not in ['upcoming', 'ongoing']:
            raise serializers.ValidationError("Reservations can only be made for upcoming or ongoing events.")

        if data.get('seats_reserved') > event.available_seats:
            raise serializers.ValidationError(f"Only {event.available_seats} seats are available for this event.")
        return data

    def create(self, validated_data):
        event = validated_data['event']

        event.available_seats-= validated_data['seats_reserved']
        event.save()

        return Reservation.objects.create(**validated_data)