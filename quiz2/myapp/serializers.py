# registration/serializers.py

from rest_framework import serializers
from .models import TemporaryLogin, Question, UserResponse, UserScore

class StepOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryLogin
        fields = ['name', 'student_no', 'email']

class StepTwoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['question', 'response']

class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['user', 'score']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer']

