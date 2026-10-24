from django.db import models

class Question(models.Model):
    content = models.CharField(max_length=200)
    grade = models.IntegerField()

    def __str__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Submission(models.Model):
    exam = models.ForeignKey(
        "Exam", on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name="submissions"
    )
    choices = models.ManyToManyField(Choice)
    total_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.student} - {self.total_score}"
