from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Quiz, Question, QuizAttempt

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type','is_staff')
    list_filter = ('user_type','is_staff','is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info',{'fields':('user_type',)}),
    )

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at') 
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'started_at', 'completed_at')
    list_filter = ('quiz', 'user')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)