from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import Friendship, DashUser

class FriendView(ViewSet):
    """DayDash API friends handling"""

    def list(self, request):
        """Handle GET requests to get friends

        Returns:
            Response -- JSON serialized list of friends
        """
        # Add additional serialization to group friends by date
        try:
            user = DashUser.objects.get(user=request.auth.user)
            friends = DashUser.objects.filter(user_friend=user)
            serialized = FriendSerializer(friends, many=True)
        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for friends
        Returns:
            Response: JSON serialized representation of newly created friend"""
                
        try:
            user = DashUser.objects.get(user=request.auth.user)
            friend = Friend.objects.create(
                name = request.data['name'],
                description = request.data['description'],
                location = request.data['location'],
                start_datetime = request.data['startDateTime'],
                end_datetime = request.data['endDateTime'],
                user = user
            )
            serialized = FriendSerializer(friend)

        except IntegrityError:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        friend = Friend.objects.get(pk=pk)
        if friend.user == DashUser.objects.get(user=request.auth.user):
            friend.name = request.data['name']
            friend.description = request.data['description']
            friend.location = request.data['location']
            friend.start_datetime = request.data['startDateTime'], timezone=timezone,
            friend.end_datetime = request.data['endDateTime'], timezone=timezone,
            friend.save()
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for friends

        Returns:
            Response: None with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            Friend.objects.get(pk=pk, user=user).delete()
        
        except (IntegrityError, ObjectDoesNotExist):
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class FriendSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    friend = serializers.StringRelatedField(source='DashUser.full_name')
    
    class Meta:
        model = DashUser
        fields = ( 'id', 'fullName')
