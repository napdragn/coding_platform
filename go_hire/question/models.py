from django.db import models

class Question(models.Model):
    question_text = models.CharField(db_index=True, max_length=200)
    description = models.TextField(null=False, blank=True)
    questions_choices = (
        ('mcq', 'Multiple Choice Question'),
        ('code', 'Coding Question')
    )
    type = models.CharField(
        max_length=30, default='code', choices=questions_choices, db_index=True)

    def __str__(self):
        return f"{self.id}: {self.question_text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    expected_input = models.TextField(null=False, blank=True)
    expected_output = models.TextField()

    def __str__(self):
        return f"{self.question.question_text}"


class Tag(models.Model):
    tag_title = models.CharField(db_index=True, max_length=40)

    def __str__(self):
        return f"{self.tag_title}"


class QuestionTagMapping(models.Model):
    question = models.ForeignKey(Question, db_index=True, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.question.question_text}: {self.tag.tag_title}"
