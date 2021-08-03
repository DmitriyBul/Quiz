from django.contrib import admin

# Register your models here.
from .models import Question, Quiz, UsersAnswer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_filter = ['name', 'id']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'id']
    list_filter = ['quiz', 'question_text', 'id']


@admin.register(UsersAnswer)
class UsersAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer']
    list_filter = ['user', 'question', 'answer']
