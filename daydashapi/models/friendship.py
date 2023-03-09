from django.db import models
from daydashapi.models import DashUser, Tag

class Friendship(models.Model):

    friender = models.ForeignKey(DashUser, on_delete=models.CASCADE, related_name='user_friend')
    friendee = models.ForeignKey(DashUser, on_delete=models.CASCADE, related_name='friended_user')
    friend_tags = models.ManyToManyField(Tag, related_name='tagged_friends')
