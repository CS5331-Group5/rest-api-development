from django.contrib.auth.models import User
from django.db import models


class Diary(models.Model):
    title = models.CharField(max_length=100)
    person = models.ForeignKey('auth.User', related_name='diary', blank=True)
    due_to = models.DateTimeField()

    def __str__(self):
        return 'Diary entry with title: {}'.format(self.title)
