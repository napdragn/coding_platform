from django.db import models

# Create your models here.
# user/models.py
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)


def __str__(self):
    return self.user.username
