from contests.api import GetContestsApi
from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("get_contests", GetContestsApi.as_view()),
    # path('', views.index, name='index'),
]
