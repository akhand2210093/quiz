from django.urls import path
from .views import StepOneView, StepTwoView, QuestionListView, SubmitResponseView, UserScoreView, LeaderboardView, QuestionCreateView

urlpatterns = [
    path('login/step-one/', StepOneView.as_view(), name='step-one'),
    path('login/step-two/', StepTwoView.as_view(), name='step-two'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit-response/', SubmitResponseView.as_view(), name='submit-response'),
    path('user-score/<str:email>/', UserScoreView.as_view(), name='user-score'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
]
