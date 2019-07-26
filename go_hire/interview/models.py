from django.db import models
from django.contrib.auth.models import User

from util.base_models import DateTimeModel


class Interview(DateTimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inteviews')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)


class Round(DateTimeModel):
    TYPE_OF_ROUND = (
        ('telephonic', 'telephonic'),
        ('f2f', 'f2f'),
        ('online_coding', 'online_coding')
    )
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    interviewee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    type = models.CharField(choices=TYPE_OF_ROUND, max_length=15)


class Feedback(DateTimeModel):
    interview_round = models.ForeignKey(Round, on_delete=models.CASCADE)
    query = models.TextField(null=True)
    feedback = models.TextField(null=True)
