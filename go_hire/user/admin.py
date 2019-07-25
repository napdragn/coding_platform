from django.contrib import admin

# Register your models here.
from django.contrib import admin


# user/admin.py
from django.contrib import admin
from user.models import UserProfileInfo, User
# Register your models here.
admin.site.register(UserProfileInfo)
