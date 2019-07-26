from django.db import models

class UserSubMissionTable(models.Model):
    user_id = models.CharField(db_index=True, max_length=200)
    contest_id = models.CharField(db_index=True, max_length=200)
    ques_id = models.CharField(db_index=True, max_length=200)
    source_code = models.TextField()
    result = models.CharField(max_length=200)
    submission_id = models.IntegerField(db_index=True, null=True)
    response = models.TextField()
    def __str__(self):
        return f"{self.id}: {self.user_id}"