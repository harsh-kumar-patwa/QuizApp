from django.urls import path
from .views import RegisterView, LoginView, QuizListCreateView, QuizDetailView, QuizAttemptView, QuizSubmitView

urlpatterns  = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/attempt/', QuizAttemptView.as_view(), name='quiz-attempt'),
    path('attempts/<int:attempt_id>/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
]