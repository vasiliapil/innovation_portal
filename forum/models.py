from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Topic(models.Model):

    Συγγραφέας = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Τίτλος = models.CharField(max_length=50)
    Περιγραφή = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.Τίτλος

class Post(models.Model):

    Συγγραφέας = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    Δημοσίευση = models.DateTimeField(default=timezone.now)
    Τίτλος = models.CharField(max_length=50, default='untitled')
    Περιεχόμενο = models.TextField(max_length=100)

    def __str__(self):
        return self.Τίτλος

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):

    Συγγραφέας = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    Δημοσίευση = models.DateTimeField(default=timezone.now)
    Περιεχόμενο = models.TextField()

    def __str__(self):
        return self.Περιεχόμενο
    
    