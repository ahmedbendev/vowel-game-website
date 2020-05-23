from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    word_name = models.CharField(max_length=20)
    word_sound = models.FileField(upload_to='word_sounds')
    vowel_number = models.IntegerField()
    vowel_name = models.CharField(max_length=2)

    def __str__(self):
        return str(self.id)


class Quiz(models.Model):
    quiz_username = models.CharField(default='Guest',max_length=100)
    quiz_number_of_word = models.IntegerField()
    quiz_sounds = models.CharField(max_length=100)
    quiz_number_of_gusses = models.IntegerField()
    quiz_time = models.DateTimeField(default=timezone.now)
    quiz_questions = models.ManyToManyField(Question)
    quiz_number_of_questions = models.IntegerField(default=10)
    quiz_number_of_current_question= models.IntegerField(default=1)
    quiz_score = models.IntegerField(default=0,)
    quiz_score_percentage = models.IntegerField(default=0,)

    def __str__(self):
        return str(self.id)