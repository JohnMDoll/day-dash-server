from django.db import models
from django.contrib.auth.models import User

class DashUser(models.Model):
    zipcode = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'