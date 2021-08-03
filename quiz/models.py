from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'quiz'
        verbose_name_plural = 'quizes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quiz:quiz_detail', args=[self.slug])


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='quiz', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=200)
    number = models.IntegerField()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)


class UsersAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.answer
