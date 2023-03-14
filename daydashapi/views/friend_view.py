from django.db.models import Q
from django.utils import timezone as django_tz
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import Friendship, DashUser, Event
from pyzipcode import ZipCodeDatabase
from datetime import timedelta


class FriendView(ViewSet):
    """DayDash API friends handling"""

    def retrieve(self, request, pk):
        """Handle GET requests to get friend

        Returns:
            Response -- JSON serialized friend object
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            friend = DashUser.objects.get(user_id=pk)
            friends = Friendship.objects.get(friender=friend, friendee=user)

            serialized = FriendSerializer(friend)

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get friends

        Returns:
            Response -- JSON serialized list of friends
        """
        # TODO: add friend search function by full_name and email
        # TODO: add function to return user frienders with impending events

        user = DashUser.objects.get(user=request.auth.user)
        try:
            if "frienders" in request.query_params:
                friends = Friendship.objects.filter(friendee=user)
                for friend in friends:

                    zcdb = ZipCodeDatabase()
                    zipcode = zcdb[friend.friender.zipcode]
                    time_shift = zipcode.timezone

                    friend.events = Event.objects.filter(user=friend.friender, start_datetime__gte=(
                        django_tz.now()+timedelta(hours=time_shift)).date()).order_by('start_datetime')

                serialized = FrienderFriendshipSerializer(
                    friends, many=True, context={'request': request})

            else:
                friends = Friendship.objects.filter(friender=user)
                serialized = FriendeeFriendshipSerializer(friends, many=True)

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for friends
        Returns:
            Response: JSON serialized representation of newly created friend"""
        # TODO: prevent duplicating friendships and self-friending
        try:
            friendship = Friendship.objects.create(
                friender=DashUser.objects.get(user=request.auth.user),
                friendee=DashUser.objects.get(
                    user__email=request.data['email'])
            )
            serialized = FriendeeFriendshipSerializer(friendship)

        except ObjectDoesNotExist:
            return Response({'message': "No matching user"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    # we may actually not need this since only tags will need updated and could be done in tag_view potentially
    # def update(self, request, pk):
    #     """Handle PUT requests for a game
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     try:
    #         user == DashUser.objects.get(user=request.auth.user)
    #         friendship
    #         tags = request.data['tags']
    #         friendship.save()
    #     except ObjectDoesNotExist:
    #         return Response(None, status=status.HTTP_401_UNAUTHORIZED)

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for friends

        Returns:
            Response: None with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            Friendship.objects.get(friendee_id=pk, friender=user).delete()

        except (IntegrityError, ObjectDoesNotExist):
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class FriendSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    name = serializers.CharField(source='full_name')

    class Meta:
        model = DashUser
        fields = ('id', 'name')


class FriendEventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    startDateTime = serializers.DateTimeField(
        source='start_datetime', format='%Y-%m-%dT%H:%M')
    endDateTime = serializers.DateTimeField(
        source='end_datetime', format='%Y-%m-%dT%H:%M')

    class Meta:
        model = Event
        fields = ('id', 'name', 'startDateTime', 'endDateTime')


class FrienderFriendshipSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    friend = FriendSerializer(source='friender')
    events = FriendEventSerializer(many=True)

    class Meta:
        model = Friendship
        fields = ('id', 'friend', 'events')


class FriendeeFriendshipSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    friend = FriendSerializer(source='friendee')

    class Meta:
        model = Friendship
        fields = ('id', 'friend')
