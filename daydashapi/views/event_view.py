from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone as django_tz
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import Event, DashUser
from pyzipcode import ZipCodeDatabase
from datetime import timedelta

class EventView(ViewSet):
    """DayDash API events handling"""

    def list(self, request):
        """Handle GET requests to get events

        Returns:
            Response -- JSON serialized list of events
        """
        # Add additional serialization to group events by date
        try:
            # need to also return friender's events somehow
            user = DashUser.objects.get(user=request.auth.user)
            #declare instance of sipcode db
            zcdb = ZipCodeDatabase()
            # get a ZipCode obj from user's zipcode
            zipcode = zcdb[user.zipcode]
            #pull the shift from UTC from zipcode obj's timezone prop
            time_shift = zipcode.timezone
            # filtering for events occurring today or in the future shifting "today" by the user's time shift
            events = Event.objects.filter(user=user, start_datetime__gte=(django_tz.now()+timedelta(hours=time_shift)).date()).order_by('start_datetime')
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
        # TODO: add exception handling
        event = Event.objects.get(pk=pk)
        user = DashUser.objects.get(user=request.auth.user)
        # event_tags = set(request.data['tags'])


        if event.user == user:
            event.name = request.data['name']
            event.description = request.data['description']
            event.location = request.data['location']
            event.start_datetime = request.data['startDateTime']
            event.end_datetime = request.data['endDateTime']
            event.tags.set(request.data['tags'])
            event.save()
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for events

        Returns:
            Response: None with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            Event.objects.get(pk=pk, user=user).delete()
        
        except (IntegrityError, ObjectDoesNotExist):
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    startDateTime = serializers.DateTimeField(source='start_datetime', format='%Y-%m-%dT%H:%M')
    endDateTime = serializers.DateTimeField(source='end_datetime', format='%Y-%m-%dT%H:%M')

    class Meta:
        model = Event
        fields = ( 'id', 'name', 'description', 'location', 'startDateTime', 'endDateTime', 'tags')
