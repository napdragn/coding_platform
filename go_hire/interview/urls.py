from interview.api import InterviewApi, RoundApi, FeedbackApi
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path("interview", InterviewApi.as_view()),
    path("round", RoundApi.as_view()),
    path("feedback", FeedbackApi.as_view()),
]
