from django.db import models
from daydashapi.models import DashUser, Event

class EventComments(models.Model):

    comment = models.CharField(max_length=255)
    commenter = models.ForeignKey(DashUser, on_delete=models.CASCADE, related_name='user_comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_comments')
