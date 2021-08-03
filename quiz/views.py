from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, View

from quiz.models import Quiz, Question


class QuizListView(ListView):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz_list = Quiz.objects.all()
        context_object_name = 'posts'
        template_name = 'quiz/quiz_list.html'
        context = {'quiz_list': quiz_list}
        return render(request, template_name, context)


class QuizDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        template_name = 'quiz/quiz_detail.html'
        number = 1
        next_number = number + 1
        context = {'quiz': quiz, 'number': number, 'next_number': next_number}
        return render(request, template_name, context)


class QuestionDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        next_number = self.kwargs['number'] + 1
        question = Question.objects.filter(number=self.kwargs['number']).get(quiz=quiz)
        template_name = 'quiz/question_detail.html'
        context = {'quiz': quiz, 'question': question, 'next_number': next_number}
        return render(request, template_name, context)


class QuestionNextDetailView(View):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        number = int(self.kwargs['number']) + 1
        question = Question.objects.filter(number=number).get(quiz=quiz)
        template_name = 'quiz/question_detail.html'
        context = {'quiz': quiz, 'question': question}
        return render(request, template_name, context)


'''
def questions_for_user(request, slug):
    quetions = Question.objects.filter(quiz=quiz)
    for question in questions:
       '''
