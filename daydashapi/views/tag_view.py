from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from daydashapi.models import DashUser, Tag


class TagView(ViewSet):
    """DayDash API tags handling"""

    def list(self, request):
        """Handle GET requests to get tags

        Returns:
            Response -- JSON serialized list of tags
        """
        # Add additional serialization to group tags by date
        try:
            user = DashUser.objects.get(user=request.auth.user)
            tags = Tag.objects.filter(user=user)
            serialized = TagsSerializer(tags, many=True)
        except ObjectDoesNotExist:
            return Response({'valid': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handles POST requests for tags
        Returns:
            Response: JSON serialized representation of newly created tag"""

        try:
            tags = Tag.objects.create(
                user=DashUser.objects.get(user=request.auth.user),
                tag=request.data['tag']
            )
            serialized = TagsSerializer(tags)

        except ObjectDoesNotExist:
            return Response({'message': "No matching user"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    # use this to both update tag names and change tags assigned to friends?
    # currently supports only renaming tags
    def update(self, request, pk):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            tag = Tag.objects.get(user=user, pk=pk)
            tag = request.data['tag']
            tag.save()
        except ObjectDoesNotExist:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for tags

        Returns:
            Response: None with 204 status code
        """
        try:
            user = DashUser.objects.get(user=request.auth.user)
            Tag.objects.get(pk=pk, user=user).delete()

        except (IntegrityError, ObjectDoesNotExist):
            return Response({'message': "Request could not be completed"}, status=status.HTTP_404_NOT_FOUND)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagFriendSerializer(serializers.ModelSerializer):
    """JSON serializer for friend tags"""
    name = serializers.CharField(source='full_name')

    class Meta:
        model = DashUser
        fields = ('id', 'name')


class TagsSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    # tag = TagFriendSerializer(source='tag')
    # tag = serializers.CharField(source='tag')

    class Meta:
        model = Tag
        fields = ('id', 'tag')
