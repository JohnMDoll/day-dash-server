from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
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
        try:
            # need to also return friender's events somehow
            user = DashUser.objects.get(user=request.auth.user)
            events = Event.objects.filter(user=user)
            serialized = EventSerializer(events, many=True)
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
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.name = request.data['name']
        event.description = request.data['description']
        event.location = request.data['location']
        event.start_datetime = request.data['startDateTime']
        event.end_datetime = request.data['endDateTime']
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
