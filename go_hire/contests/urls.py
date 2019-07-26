from contests.api import GetContestsApi, BeginContestApi, SubmitContestApi
from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("get_contests", GetContestsApi.as_view()),
    path("begin_contest", BeginContestApi.as_view()),
    path("submit_contest", SubmitContestApi.as_view()),
]
