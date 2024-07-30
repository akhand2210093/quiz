from django.db import models
from django.utils import timezone
import random

class TemporaryLogin(models.Model):
    name = models.CharField(max_length=255)
    student_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()
    
    def otp_is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300  # OTP is valid for 5 minutes

class Question(models.Model):
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)

class UserResponse(models.Model):
    user = models.ForeignKey(TemporaryLogin, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)

class UserScore(models.Model):
    user = models.ForeignKey(TemporaryLogin, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

