from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, Quiz, Question, QuizAttempt
from .serializers import UserSerializer, QuizSerializer, QuestionSerializer, QuizAttemptSerializer  

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes  = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class QuizListCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.user_types != 'admin':
            return Response({'error': 'You are not authorized to create quiz'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuizDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return None
    
    def get(self, request, pk):

        quiz = self.get_object(pk)
        if quiz:
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        if request.user.user_types != 'admin':
            return Response({'error': 'You are not authorized to update quiz'}, status=status.HTTP_403_FORBIDDEN)
        
        quiz = self.get_object(pk)
        if not quiz:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if request.user.user_types != 'admin':
            return Response({'error': 'You are not authorized to delete quiz'}, status=status.HTTP_403_FORBIDDEN)
        
        quiz = self.get_object(pk)
        if quiz:
            quiz.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
    

class QuizAttemptView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        
        quiz_attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
        serializer = QuizAttemptSerializer(quiz_attempt)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class QuizSubmitView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, attempt_id):
        try:
            attempt = QuizAttempt.objects.get(pk=attempt_id,user = request.user)
        except QuizAttempt.DoesNotExist:
            return Response({'error': 'Quiz attempt not found'}, status=status.HTTP_404_NOT_FOUND)
        
        answers = request.data.get('answers', {})
        correct_count = 0
        total_questions = attempt.quiz.questions.count()

        for question in attempt.quiz.questions.all():
            user_answer = answers.get(str(question.id))
            if user_answer == question.correct_answer:
                correct_count += 1
        
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        attempt.answers = answers
        attempt.score = score
        attempt.completed_at = timezone.now()
        attempt.save()

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data)
    

