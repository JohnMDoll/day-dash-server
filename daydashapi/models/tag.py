from django.db import models
from daydashapi.models import DashUser

class Tag(models.Model):

    user = models.ForeignKey(DashUser, on_delete=models.CASCADE, related_name='user_tags')
    tag = models.CharField(max_length=15)
