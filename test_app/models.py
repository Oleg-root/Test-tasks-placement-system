import os.path

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# each class is an each own table in database
# each field is a different field in the datable

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.FileField(upload_to='attached_tasks', default='NULL')

    def __str__(self):
        return self.title

    def filename(self):
        return os.path.basename(self.task.name)

    def get_absolute_url(self):
        return reverse('vacancy-detail', kwargs={'pk': self.pk}) # full path as a string

    def delete(self, *args, **kwargs):
        self.task.delete()
        try:
            Solution.objects.get(associated_vacancy=self).file.delete()
        except:
            pass
        super().delete(*args, **kwargs)


class Solution(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=100)
    associated_vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, default=0)
    file = models.FileField(upload_to='solutions', default=0)
    responded = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author.username} -> {self.receiver}'

    def filename(self):
        return os.path.basename(self.file.name)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

class Response(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=100)
    associated_solution = models.ForeignKey(Solution, on_delete=models.CASCADE, default=0)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author.username} -> {self.receiver}'

class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

