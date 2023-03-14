from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import Friendship, DashUser, Event, EventComments


class CommentView(ViewSet):
    """DayDash API comment handling"""

    def retrieve(self, request, pk):
        """Handle GET requests to get comment

        Returns:
            Response -- JSON serialized comment object
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            event = Event.objects.get(pk=request.data['event'])
            comment = request.data['comment']

            serialized = FriendSerializer(friend)

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get comments

        Returns:
            Response -- JSON serialized list of comments
        """
        # TODO: add comment visibility for friend's events only when comments are made by the friend or friend-friends that share friendTags with the user 

        user = DashUser.objects.get(user=request.auth.user)
        try:
            # if "frienders" in request.query_params:
            #     friends = Friendship.objects.filter(friendee=user)
            #     for friend in friends:

            #         zcdb = ZipCodeDatabase()
            #         zipcode = zcdb[friend.friender.zipcode]
            #         time_shift = zipcode.timezone

            #         friend.events = Event.objects.filter(user=friend.friender, start_datetime__gte=(
            #             django_tz.now()+timedelta(hours=time_shift)).date()).order_by('start_datetime')

            #     serialized = FrienderFriendshipSerializer(
            #         friends, many=True, context={'request': request})

            # else:
            friends = Friendship.objects.filter(friender=user)
            serialized = EventCommentSerializer(friends, many=True)

        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for comment
        Returns:
            Response: JSON serialized representation of newly created comment"""
        try:
            new_comment = EventComments.objects.create(
                commenter = DashUser.objects.get(user=request.auth.user),
                event = Event.objects.get(pk=request.data['event']),
                comment = request.data['comment']
                )

            serialized = EventCommentSerializer(new_comment)

        except ObjectDoesNotExist:
            return Response({'message': "No matching user"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a comment
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            comment = EventComments.objects.get(pk=pk)
            comment.comment = request.data['comment']
            comment.save()
        except ObjectDoesNotExist:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a comment

        Returns:
            Response: None with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            EventComments.objects.get(commenter=user, pk=pk).delete()

        except (IntegrityError, ObjectDoesNotExist):
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommenterSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    name = serializers.CharField(source='full_name')

    class Meta:
        model = DashUser
        fields = ('id', 'name')

class CommentEventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    class Meta:
        model = Event
        fields = ('id',)

class EventCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for friends"""
    commenter = CommenterSerializer()

    class Meta:
        model = EventComments
        fields = ('id', 'event', 'comment', 'commenter')
