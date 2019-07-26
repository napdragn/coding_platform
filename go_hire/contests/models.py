from django.db import models
from question.models import Question
from util import base_models

class Contest(base_models.DateTimeModel):
    title = models.CharField(db_index=True, max_length=100)

    def __str__(self):
        return f"{self.id}: {self.title}"


class ContestQuestionMapping(base_models.DateTimeModel):
    contest = models.ForeignKey(Contest, db_index=True, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.contest}: {self.question.question_text}"


class UserContest(base_models.DateTimeModel):
    email = models.EmailField(null=False, db_index=True)
    contest = models.ForeignKey(Contest, db_index=True, on_delete=models.PROTECT)
    contest_duration = models.PositiveIntegerField(default=2)
    user_start_time = models.DateTimeField(null=True, blank=True)
    user_end_time = models.DateTimeField(null=True, blank=True)
    result = models.CharField(default="not_started", null=True, max_length=40)
