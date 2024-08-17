from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import TemporaryLogin, Question, UserResponse, UserScore
from .serializers import StepOneSerializer, StepTwoSerializer, QuestionSerializer, UserResponseSerializer, UserScoreSerializer, QuestionCreateSerializer

class StepOneView(APIView):
    def post(self, request):
        serializer = StepOneSerializer(data=request.data)
        if serializer.is_valid():
            temp_login = serializer.save()
            temp_login.generate_otp()
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {temp_login.otp}',
                'from@example.com',
                [temp_login.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StepTwoView(APIView):
    def post(self, request):
        serializer = StepTwoSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            temp_login = get_object_or_404(TemporaryLogin, email=email, otp=otp)
            if temp_login.otp_is_valid():
                # # Generate JWT token
                # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                # payload = jwt_payload_handler(temp_login)
                # token = jwt_encode_handler(payload)
                # return Response({'token': token}, status=status.HTTP_200_OK)
                # Generate JWT token
                refresh = RefreshToken.for_user(temp_login)
                access_token = str(refresh.access_token)
                return Response({'access': access_token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'OTP is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

class SubmitResponseView(APIView):
    def post(self, request):
        user_email = request.data.get('email')
        user = get_object_or_404(TemporaryLogin, email=user_email)
        serializer = UserResponseSerializer(data=request.data)
        if serializer.is_valid():
            user_response = serializer.save(user=user)
            user_response.correct = user_response.response == user_response.question.correct_answer
            user_response.save()
            # Update user score
            user_score, created = UserScore.objects.get_or_create(user=user)
            if user_response.correct:
                user_score.score += 4  # Correct answer
            else:
                user_score.score -= 1  # Wrong answer
            user_score.save()
            return Response({'message': 'Response submitted'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserScoreView(APIView):
    def get(self, request, email):
        user = get_object_or_404(TemporaryLogin, email=email)
        user_score = get_object_or_404(UserScore, user=user)
        serializer = UserScoreSerializer(user_score)
        return Response(serializer.data)

class LeaderboardView(APIView):
    def get(self, request):
        top_scores = UserScore.objects.order_by('-score')[:100]  # Top 10 scores
        serializer = UserScoreSerializer(top_scores, many=True)
        return Response(serializer.data)

class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
