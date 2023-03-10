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
        # TODO: add friend search function by full_name and email
        # TODO: add function to return user frienders with impending events

        user = DashUser.objects.get(user=request.auth.user)

        if "frienders" in request.query_params:
            friends = Friendship.objects.filter(friendee=user)
            serialized = FrienderFriendshipSerializer(friends, many=True)
        else:
            try:
                friends = Friendship.objects.filter(friender=user)
                serialized = FriendeeFriendshipSerializer(friends, many=True)
            except ObjectDoesNotExist:
                return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for friends
        Returns:
            Response: JSON serialized representation of newly created friend"""
        # TODO: prevent duplicating friendships
        try:
            friendship = Friendship.objects.create(
                friender=DashUser.objects.get(user=request.auth.user),
                friendee=DashUser.objects.get(user__email=request.data['email'])
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

class FrienderFriendshipSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    friend = FriendSerializer(source='friender')
    # friend = serializers.CharField(source='friendee')

    class Meta:
        model = Friendship
        fields = ('id', 'friend')

class FriendeeFriendshipSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    friend = FriendSerializer(source='friendee')
    # friend = serializers.CharField(source='friendee')

    class Meta:
        model = Friendship
        fields = ('id', 'friend')
