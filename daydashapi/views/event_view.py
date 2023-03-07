from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import Event, DashUser

class EventView(ViewSet):
    """DayDash API events handling"""

    def list(self, request):
        """Handle GET requests to get events

        Returns:
            Response -- JSON serialized list of events
        """

        # need some check for user and some empty return if none?
        try:
            user = request.auth.user
            if "park_id" in request.query_params:
                event = ParkEvent.objects.get(park_id=request.query_params['park_id'], user=user)
                serialized = ParkEventSerializer(event)

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for events
        Returns:
            Response: JSON serialized representation of newly created event"""
        try:
            user = DashUser.objects.get(user=request.auth.user)
            event = Event.objects.create(
                name = request.data['name'],
                description = request.data['description'],
                location = request.data['location'],
                start_datetime = request.data['startDateTime'],
                end_datetime = request.data['endDateTime'],
                user = user
            )
            serialized = EventSerializer(event)

        except IntegrityError:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle PUT requests for service tickets

        Returns:
            Response: None with 204 status code
        """
        try:
            user = request.auth.user
            if "park_id" in request.data:
                event = ParkEvent.objects.get(park_id=request.data['park_id'], user=user)
            else:
                return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
            event.delete()
        except (IntegrityError, ObjectDoesNotExist):
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event photos"""
    startDateTime = serializers.CharField(source='start_datetime')
    endDateTime = serializers.CharField(source='end_datetime')

    class Meta:
        model = Event
        fields = ( 'id', 'name', 'description', 'location', 'startDateTime', 'endDateTime')
