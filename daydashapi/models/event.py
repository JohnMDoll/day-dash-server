from django.db import models
from daydashapi.models import DashUser, Tag

class Event(models.Model):
    """Event class

    Args:
        name = CharField(max_length=255),
        description = CharField(max_length=500, null=True),
        location = CharField(max_length=500, null=True),
        start_datetime = DateTimeField(),
        end_datetime = DateTimeField(null=True),
        user = ForeignKey(DashUser, on_delete=CASCADE, related_name='user_events'),
        tags = ManyToManyField(Tag, related_name='event_tags'),
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True)
    location = models.CharField(max_length=500, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(DashUser, on_delete=models.CASCADE, related_name='user_events')
    tags = models.ManyToManyField(Tag, related_name='event_tags')
