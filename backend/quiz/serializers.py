from rest_framework import serializers
from .models import User, Quiz, Question, QuizAttempt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_type', 'text', 'options', 'correct_answer', 'order')

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'created_by','created_at','updated_at','questions')

class QuizAttemptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ('id', 'user', 'quiz', 'score', 'answers', 'started_at', 'completed_at')    
