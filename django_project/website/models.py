from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User

SUBJECTS = (('maths','Maths'),('physics','Physics'),('chemistry','Chemistry'),('cse','Computer Science'),('eee','Electronics and Electrical'),('ece','Communications'),('mech','Mechanics'))

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=20, choices=SUBJECTS, default='none')
    teachers = models.CharField(max_length=300, default='none')

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})    

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    answered_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('answer-detail', kwargs={'pk': self.pk})

