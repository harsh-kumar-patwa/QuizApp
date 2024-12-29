from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('admin','Admin'),
        ('user','User'),
    )
    user_type = models.CharField(max_length=5, choices=USER_TYPES, default='user') 

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    Question_Type = (
        ('mcq','MCQ'),
        ('multiple','Multiple Answer'),
        ('true_false','True/False'),
        ('text','Text Answer'), 
    )

    quiz = models.ForeignKey(Quiz,related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=Question_Type)
    text = models.TextField()
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.JSONField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    answers = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']