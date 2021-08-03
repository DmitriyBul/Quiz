from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', lambda req: redirect('/home/')),
    path('home/', views.QuizListView.as_view(), name='quiz_list'),
    path('<slug:slug>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('<slug:slug>/<int:number>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<slug:slug>/<int:number>/', views.QuestionNextDetailView.as_view(), name='next_question_detail'),
]
