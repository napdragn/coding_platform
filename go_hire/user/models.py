from django.db import models

# Create your models here.
# user/models.py
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    ctc = models.CharField(blank=True, max_length=10)
    current_company = models.CharField(blank=True, max_length=50)
    resume = models.FileField(upload_to='resumes', blank=True)
    name = models.CharField(blank=True, max_length=50)


def __str__(self):
    return self.user.username
