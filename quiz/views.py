from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, View

from quiz.forms import UserAnswerForm
from quiz.models import Quiz, Question, UsersAnswer


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
        context = {'quiz': quiz}
        return render(request, template_name, context)


class QuestionDetailView(View, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        next_number = 1
        question = Question.objects.filter(number=1).get(quiz=quiz)
        UsersAnswer.objects.filter(user=request.user).delete()
        form = UserAnswerForm(request.POST, user=request.user, question=question)
        template_name = 'quiz/question_detail.html'
        context = {'quiz': quiz, 'question': question, 'next_number': next_number, 'form': form}
        return render(request, template_name, context)

    def post(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        question = Question.objects.filter(number=1).get(quiz=quiz)
        form = UserAnswerForm(request.POST, user=request.user, question=question)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.question = question
            new_item.save()
            return redirect('quiz:next_question_detail', slug=self.kwargs['slug'], number=question.number)


class QuestionNextDetailView(View, LoginRequiredMixin):
    def get(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        number = int(self.kwargs['number']) + 1
        question = Question.objects.filter(number=self.kwargs['number']).get(quiz=quiz)
        questions_count = Question.objects.filter(quiz=quiz).count()
        form = UserAnswerForm(request.POST, user=request.user, question=question)
        if number <= questions_count:
            question = Question.objects.filter(number=number).get(quiz=quiz)
            template_name = 'quiz/question_detail.html'
            context = {'quiz': quiz, 'question': question, 'form': form}
            return render(request, template_name, context)
        else:
            question_ids = list(Question.objects.filter(quiz=quiz).values_list('id', flat=True))
            correct_answers = list(
                Question.objects.filter(quiz=quiz).values_list('answer', flat=True).order_by('number'))
            users_answers = list(UsersAnswer.objects.filter(question__id__in=question_ids).values_list('answer',
                                                                                                       flat=True))
            correct_answers_count = 0
            number_of_questions = len(question_ids)
            for item in range(number_of_questions):
                if correct_answers[item] == users_answers[item]:
                    correct_answers_count += 1
            template_name = 'quiz/results.html'
            context = {'quiz': quiz, 'correct_answers_count': correct_answers_count,
                       'number_of_questions': number_of_questions}
            return render(request, template_name, context)

    def post(self, request, ordering='AZ', *args, **kwargs):
        quiz = Quiz.objects.get(slug=self.kwargs['slug'])
        question = Question.objects.filter(number=self.kwargs['number']).get(quiz=quiz)
        question2 = Question.objects.filter(number=self.kwargs['number'] + 1).get(quiz=quiz)
        form = UserAnswerForm(request.POST, user=request.user, question=question2)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.question = question2
            new_item.save()
            return redirect('quiz:next_question_detail', slug=self.kwargs['slug'], number=question.number + 1)
