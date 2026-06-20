from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return self.name or self.user.username
